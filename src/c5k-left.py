import board
import busio
import digitalio
import time
from adafruit_mcp230xx.mcp23008 import MCP23008
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode

# ─── Hardware setup ──────────────────────────────────────────────────────────
vcc = digitalio.DigitalInOut(board.VCC_OFF)
vcc.direction = digitalio.Direction.OUTPUT
vcc.value = True
time.sleep(0.5)

i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
mcp = MCP23008(i2c)
pins = [mcp.get_pin(i) for i in range(5)]
for p in pins:
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP

# ─── BLE HID setup ─────────────────────────────────────────────────────────────
ble = adafruit_ble.BLERadio()
hid_svc = HIDService()
advert = ProvideServicesAdvertisement(hid_svc)
keyboard = Keyboard(hid_svc.devices)
mouse = Mouse(hid_svc.devices)

ble.start_advertising(advert)
while not ble.connected:
    pass
ble.stop_advertising()

# ─── Timing constants ─────────────────────────────────────────────────────────
STABLE_MS_ALPHA = 0.03   # 30 ms for layer-1 (alpha)
STABLE_MS_OTHER = 0.02   # 20 ms for layers 2/3
DEBOUNCE_UP      = 0.05  # pause after send
TAP_WINDOW       = 0.5   # thumb-tap window
MIN_TAP_INT      = 0.1   # thumb debounce

# ─── Mouse & Movement Setup for layer-5 ─────────────────────────────────────────
MOVE_DELTA = 5  # pixels per move step

mouse_button_chords = {
    (0,1): Mouse.LEFT_BUTTON,
    (2,3): Mouse.RIGHT_BUTTON,
    (1,2): Mouse.MIDDLE_BUTTON,
    (0,4): Mouse.BACK_BUTTON,
    (3,4): Mouse.FORWARD_BUTTON,
}

mouse_move_chords = {
    (0,): (-MOVE_DELTA,  0),   # left
    (1,): ( MOVE_DELTA,  0),   # right
    (2,): (       0, -MOVE_DELTA),  # up
    (3,): (       0,  MOVE_DELTA),  # down
}

mouse_scroll_chords = {
    (0,3):  1,   # scroll up
    (3,4): -1,   # scroll down
}

mouse_hold_chords = {
    (0,1,4): Mouse.LEFT_BUTTON,  # click-&-hold for drag
}

mouse_release_chords = {
    (1,2,4): Mouse.LEFT_BUTTON,  # release drag
}


# ─── State variables ──────────────────────────────────────────────────────────
layer            = 1     # layers 1..5
thumb_taps       = 0
last_combo       = ()
pending_combo    = None
sent_release     = False
last_time        = 0
modifier_armed   = False
held_modifier    = None
scag_skip_combo  = None
skip_scag        = False

# ─── Chord maps for layers 1–3 ─────────────────────────────────────────────────
layer_maps = [
    {},  # dummy index 0
    { # layer-1: letters
      (0,):Keycode.E,(1,):Keycode.I,(2,):Keycode.A,(3,):Keycode.S,
      (0,1):Keycode.R,(0,2):Keycode.O,(0,3):Keycode.C,(1,2):Keycode.N,
      (1,3):Keycode.L,(2,3):Keycode.T,(0,1,2):Keycode.D,(1,2,3):Keycode.P,
      (0,1,2,3):Keycode.U,(0,2,3):Keycode.SPACE,(0,1,3):Keycode.BACKSPACE,
      (0,4):Keycode.M,(1,4):Keycode.G,(2,4):Keycode.H,(3,4):Keycode.B,
      (0,1,4):Keycode.Y,(0,2,4):Keycode.W,(0,3,4):Keycode.X,
      (1,2,4):Keycode.F,(1,3,4):Keycode.K,(2,3,4):Keycode.V,
      (0,1,2,4):Keycode.J,(1,2,3,4):Keycode.Z,(0,1,2,3,4):Keycode.Q
    },
    { # layer-2: numbers & arrows
      (0,):Keycode.ONE,(1,):Keycode.TWO,(2,):Keycode.THREE,(3,):Keycode.FOUR,
      (0,1):Keycode.FIVE,(1,2):Keycode.SIX,(2,3):Keycode.SEVEN,(0,2):Keycode.EIGHT,
      (1,3):Keycode.NINE,(0,1,2):Keycode.ZERO,
      (0,3):Keycode.UP_ARROW,(1,2,3):Keycode.DOWN_ARROW,
      (0,1,3):Keycode.RIGHT_ARROW,(0,2,3):Keycode.LEFT_ARROW,
      (0,1,2,3):Keycode.ESCAPE
    },
    { # layer-3: whitespace & delimiters
      (0,): Keycode.ESCAPE,(1,):Keycode.TAB,(2,):Keycode.PERIOD,(3,):Keycode.MINUS,
      (2,3):Keycode.FORWARD_SLASH,(0,1):Keycode.ENTER,(0,2):Keycode.COMMA,
      (1,3):Keycode.LEFT_BRACKET,(0,3):Keycode.RIGHT_BRACKET,
      (1,2,3):Keycode.BACKSLASH,(1,2):Keycode.BACKSPACE,
      (0,1,3):Keycode.QUOTE,(0,2,3):Keycode.SEMICOLON,(0,1,2,3):Keycode.GRAVE_ACCENT
    }
]

# ─── Modifier chords for layer-4 (SCAG) ─────────────────────────────────────────
modifier_chords = {
    (3,): Keycode.LEFT_SHIFT,
    (2,): Keycode.LEFT_CONTROL,
    (1,): Keycode.LEFT_ALT,
    (0,): Keycode.LEFT_GUI
}

# ─── Core chord logic ───────────────────────────────────────────────────────────
def check_chords():
    global layer, thumb_taps, last_combo, pending_combo
    global sent_release, last_time, modifier_armed, held_modifier
    global scag_skip_combo, skip_scag

    now = time.monotonic()
    pressed = [not p.value for p in pins]

    # 1) thumb tap logic for layer switching
    # (existing code here…)

    # 2) chord detect & stabilize
    combo = tuple(i for i,b in enumerate(pressed) if b)
    if combo != last_combo:
        last_time = now
        if last_combo == () and combo != ():
            pending_combo = None
            sent_release = False
    ms = STABLE_MS_ALPHA if layer == 1 else STABLE_MS_OTHER
    if combo and (now - last_time) >= ms and combo != pending_combo:
        pending_combo = combo

    # 3) layer-5 mouse handling
    if layer == 5:
        # 1) Movement
        if combo in mouse_move_chords:
            dx, dy = mouse_move_chords[combo]
            mouse.move(x=dx, y=dy)
            time.sleep(DEBOUNCE_UP)
            return

        # 2) Scroll
        if combo in mouse_scroll_chords:
            wheel = mouse_scroll_chords[combo]
            mouse.move(wheel=wheel)
            time.sleep(DEBOUNCE_UP)
            return

        # 3) Click-&-hold (start drag)
        if combo in mouse_hold_chords:
            mouse.press(mouse_hold_chords[combo])
            return

        # 4) Release click (end drag)
        if combo in mouse_release_chords:
            mouse.release(mouse_release_chords[combo])
            return

        # 5) Simple clicks
        if combo in mouse_button_chords:
            mouse.click(mouse_button_chords[combo])
            time.sleep(DEBOUNCE_UP)
            return

    # 4) SCAG logic for layer-4
    # (existing code here…)

    # 5) layer 1–3 handling
    # (existing code here…)

    # 6) clear on full release
    if combo == () and last_combo != ():
        pending_combo = None
        sent_release = False

    last_combo = combo

# ─── Main loop ────────────────────────────────────────────────────────────────
while ble.connected:
    check_chords()
    time.sleep(0.01)
