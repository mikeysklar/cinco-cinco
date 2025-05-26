import board
import busio
import time
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ─────────────────────────────────────────────────────────────────────────────
# Turn on external VCC (if needed)
vcc_enable = digitalio.DigitalInOut(board.VCC_OFF)
vcc_enable.direction = digitalio.Direction.OUTPUT
vcc_enable.value = True
time.sleep(0.5)

# ─────────────────────────────────────────────────────────────────────────────
# I2C + MCP23008 on pins 0–4
i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
mcp = MCP23008(i2c)
pins = [mcp.get_pin(i) for i in range(5)]
for p in pins:
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP

# ─────────────────────────────────────────────────────────────────────────────
# BLE HID setup
ble = adafruit_ble.BLERadio()
hid_service   = HIDService()
advertisement = ProvideServicesAdvertisement(hid_service)
keyboard      = Keyboard(hid_service.devices)

ble.start_advertising(advertisement)
while not ble.connected:
    pass
ble.stop_advertising()

# ─────────────────────────────────────────────────────────────────────────────
# State tracking
pin_to_idx       = {i: i for i in range(5)}  # MCP pin → index
pressed          = [False] * 5

NUM_LAYERS       = 5
COOLDOWN         = 0.05    # after sending a key
TAP_WINDOW       = 0.5     # max sec between thumb taps
LAYER_TIMEOUT    = 1.0     # auto-reset if no chord in this many sec
thumb_taps       = 0
last_tap_time    = 0
last_thumb_state = False
layer            = 0
pending          = None

# ─────────────────────────────────────────────────────────────────────────────
# Chord → Keycode maps for each layer
layer_maps = [
    # ─── Layer 0: finger-only + thumb combos ───
    {
        # finger only (pins 0–3)
        (0,): Keycode.E,   (1,): Keycode.I,   (2,): Keycode.A,
        (3,): Keycode.S,   (0,1): Keycode.R,  (0,2): Keycode.O,
        (0,3): Keycode.C,  (1,2): Keycode.N,  (1,3): Keycode.L,
        (2,3): Keycode.T,  (0,1,2): Keycode.D,(1,2,3): Keycode.P,
        (0,1,2,3): Keycode.U,

        # thumb (pin 4) combos
        (0,4): Keycode.M,  (1,4): Keycode.G,  (2,4): Keycode.H,
        (3,4): Keycode.B,
        (0,1,4): Keycode.Y,(0,2,4): Keycode.W,(0,3,4): Keycode.X,
        (1,2,4): Keycode.F,(1,3,4): Keycode.K,(2,3,4): Keycode.V,
        (0,1,2,4): Keycode.J,(1,2,3,4): Keycode.Z,
        (0,1,2,3,4): Keycode.Q
    },
    # ─── Layers 1–4: fill with your own maps ───
    {}, {}, {}, {}
]

# ─────────────────────────────────────────────────────────────────────────────
def check_chords():
    global layer, thumb_taps, last_tap_time, last_thumb_state, pending

    now = time.monotonic()

    # 0) Auto-reset by timeout if still in a higher layer with no chord
    if layer > 0 and (now - last_tap_time) > LAYER_TIMEOUT and not any(pressed):
        layer = 0
        thumb_taps = 0
        pending = None

    # 1) sample all MCP pins
    for pin, idx in pin_to_idx.items():
        pressed[idx] = not pins[pin].value  # True == pressed

    # detect a pure thumb press (pin 4 alone)
    current_thumb = pressed[4]
    pure_thumb    = current_thumb and not any(pressed[i] for i in range(4))

    # ── A) count solo-thumb rising edges for multi-tap layer switching
    if pure_thumb and not last_thumb_state:
        # new tap or reset?
        if now - last_tap_time < TAP_WINDOW:
            thumb_taps += 1
        else:
            thumb_taps = 1
        last_tap_time = now

        # only switch once taps > 1
        if thumb_taps > 1:
            new_layer = min(thumb_taps - 1, NUM_LAYERS - 1)
            if new_layer != layer:
                layer = new_layer
                pending = None
                print(f"→ switched to layer {layer}")
        last_thumb_state = True
        return

    # clear edge-detector when thumb is released
    if not current_thumb:
        last_thumb_state = False

    # ── B) build current combo
    combo = tuple(i for i, down in enumerate(pressed) if down)

    if combo:
        # B1) in layer>0? send and auto-reset
        if layer > 0 and combo in layer_maps[layer]:
            keyboard.press(layer_maps[layer][combo])
            keyboard.release_all()
            # back to home
            layer = 0
            thumb_taps = 0
            pending = None
            time.sleep(COOLDOWN)
            return

        # B2) in layer 0? handle your finger & thumb chords
        if layer == 0 and combo in layer_maps[0]:
            if combo != pending:
                keyboard.press(layer_maps[0][combo])
                keyboard.release_all()
                pending = combo
                time.sleep(COOLDOWN)
            return

    # ── C) nothing pressed → clear pending chord
    pending = None

# ─────────────────────────────────────────────────────────────────────────────
# Main loop: poll while BLE is connected
while ble.connected:
    check_chords()
    time.sleep(0.01)
