import board
import busio
import digitalio
import time
from adafruit_mcp230xx.mcp23008 import MCP23008
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ─── Power on the MCP VCC ─────────────────────────────────────────────────────
vcc = digitalio.DigitalInOut(board.VCC_OFF)
vcc.direction = digitalio.Direction.OUTPUT
vcc.value = True
time.sleep(0.5)

# ─── I2C + MCP23008 setup ─────────────────────────────────────────────────────
i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
mcp = MCP23008(i2c)
pins = [mcp.get_pin(i) for i in range(5)]
for p in pins:
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP

# ─── BLE HID setup ─────────────────────────────────────────────────────────────
ble       = adafruit_ble.BLERadio()
hid_svc   = HIDService()
advert    = ProvideServicesAdvertisement(hid_svc)
keyboard  = Keyboard(hid_svc.devices)
ble.start_advertising(advert)
while not ble.connected:
    pass
ble.stop_advertising()

# ─── Timing & state constants ─────────────────────────────────────────────────
STABLE_MS        = 0.03    # chord settle (30ms)
DEBOUNCE_UP      = 0.05    # post-send pause
TAP_WINDOW       = 0.5     # thumb tap window
MIN_TAP_INTERVAL = 0.1     # tap debounce

# ─── State variables ──────────────────────────────────────────────────────────
layer            = 0       # 0..2 locked modes
thumb_taps       = 0
last_tap_time    = 0.0
last_combo       = ()
pending_combo    = None
sent_on_release  = False
last_change_time = time.monotonic()
last_thumb_state = False

# ─── chord→Keycode maps for layers 0–2 ────────────────────────────────────────
layer_maps = [
    { # Layer 0: alpha + space/backspace
        (0,): Keycode.E, (1,): Keycode.I, (2,): Keycode.A, (3,): Keycode.S,
        (0,1): Keycode.R,(0,2):Keycode.O,(0,3):Keycode.C,(1,2):Keycode.N,
        (1,3):Keycode.L,(2,3):Keycode.T,(0,1,2):Keycode.D,(1,2,3):Keycode.P,
        (0,1,2,3):Keycode.U,(0,2,3):Keycode.SPACE,(0,1,3):Keycode.BACKSPACE,
        (0,4):Keycode.M,(1,4):Keycode.G,(2,4):Keycode.H,(3,4):Keycode.B,
        (0,1,4):Keycode.Y,(0,2,4):Keycode.W,(0,3,4):Keycode.X,
        (1,2,4):Keycode.F,(1,3,4):Keycode.K,(2,3,4):Keycode.V,
        (0,1,2,4):Keycode.J,(1,2,3,4):Keycode.Z,(0,1,2,3,4):Keycode.Q
    },
    { # Layer 1: numbers & arrows
        (0,):Keycode.ONE,(1,):Keycode.TWO,(2,):Keycode.THREE,(3,):Keycode.FOUR,
        (0,1):Keycode.FIVE,(1,2):Keycode.SIX,(2,3):Keycode.SEVEN,(0,2):Keycode.EIGHT,
        (1,3):Keycode.NINE,(0,1,2):Keycode.ZERO,
        (0,3):Keycode.UP_ARROW,(1,2,3):Keycode.DOWN_ARROW,
        (0,1,3):Keycode.RIGHT_ARROW,(0,2,3):Keycode.LEFT_ARROW,(0,1,2,3):Keycode.ESCAPE
    },
    { # Layer 2: whitespace & delimiters
        (1,):Keycode.TAB,(2,):Keycode.PERIOD,(3,):Keycode.MINUS,
        (2,3):Keycode.FORWARD_SLASH,(0,1):Keycode.ENTER,(0,2):Keycode.COMMA,
        (1,3):Keycode.LEFT_BRACKET,(0,3):Keycode.RIGHT_BRACKET,
        (1,2,3):Keycode.BACKSLASH,(1,2):Keycode.BACKSPACE,
        (0,1,3):Keycode.QUOTE,(0,2,3):Keycode.SEMICOLON,(0,1,2,3):Keycode.GRAVE_ACCENT
    }
]

# ─── Chord detection & layer-lock logic ────────────────────────────────────────
def check_chords():
    global layer, thumb_taps, last_tap_time, last_thumb_state
    global last_combo, pending_combo, sent_on_release, last_change_time

    now = time.monotonic()
    pressed = tuple(not p.value for p in pins)
    finger_down = any(pressed[:4])
    thumb_down  = pressed[4]

        # 1) thumb-alone detect for locking
    if thumb_down and not finger_down and not last_thumb_state:
        # rising edge of sole thumb
        if (now - last_tap_time) < TAP_WINDOW:
            thumb_taps += 1
        else:
            thumb_taps = 1
        last_tap_time = now
        # lock layer: 1 tap->L0,2->L1,3->L2
        layer = min(thumb_taps-1, 2)
        print(f"→ locked to layer {layer}")
        # reset chord state
        last_combo = ()
        pending_combo = None
        sent_on_release = False
        last_thumb_state = True
        return

    if not thumb_down:
        last_thumb_state = False

    # 2) chord build & stabilize
    combo = tuple(i for i,b in enumerate(pressed) if b)
    if combo != last_combo:
        last_change_time = now
        if last_combo == () and combo != ():
            pending_combo = None
            sent_on_release = False
    if combo and (now - last_change_time) >= STABLE_MS and combo != pending_combo:
        pending_combo = combo

    # 3) send on first release
    if len(combo) < len(last_combo) and last_combo and not sent_on_release:
        # ignore pure thumb combos
        use = pending_combo or last_combo
        if use != (4,):
            kc = layer_maps[layer].get(use)
            if kc:
                keyboard.press(kc)
                keyboard.release_all()
            else:
                print(f"Unknown L{layer}: {use}")
        sent_on_release = True
        time.sleep(DEBOUNCE_UP)

    # 4) clear state on full release
    if combo == () and last_combo != ():
        pending_combo = None
        sent_on_release = False

    last_combo = combo

# ─── Main loop ────────────────────────────────────────────────────────────────
while ble.connected:
    check_chords()
    time.sleep(0.01)

