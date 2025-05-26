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

# --- Turn on external VCC (P0.13 high) ---
vcc_enable = digitalio.DigitalInOut(board.VCC_OFF)
vcc_enable.direction = digitalio.Direction.OUTPUT
vcc_enable.value = True
time.sleep(0.5)

# I2C + MCP23008 on pins 0–4 only
i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
mcp = MCP23008(i2c)
pins = [mcp.get_pin(i) for i in range(5)]
for p in pins:
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP

# --- BLE HID setup ---
ble = adafruit_ble.BLERadio()
hid = HIDService()
adv = ProvideServicesAdvertisement(hid)
kbd = Keyboard(hid.devices)

ble.start_advertising(adv)
while not ble.connected:
    pass
ble.stop_advertising()

# Map pin → index
pin_to_idx = {i: i for i in range(5)}
pressed = [False] * 5

# Layer management
NUM_LAYERS = 5
layer = 0
last_switch = 0
SWITCH_DEBOUNCE = 0.3  # seconds

# Define your chord → Keycode maps for each of the 5 layers:
# Layer 0: original mapping for pins 0–3
# Define chord → Keycode maps for each of the 5 layers:
layer_maps = [
    # ─── Layer 0: finger-only + thumb combos ───
    {
        # finger-only
        (0,): Keycode.E,   (1,): Keycode.I,   (2,): Keycode.A,
        (3,): Keycode.S,   (0,1): Keycode.R,  (0,2): Keycode.O,
        (0,3): Keycode.C,  (1,2): Keycode.N,  (1,3): Keycode.L,
        (2,3): Keycode.T,  (0,1,2): Keycode.D,(1,2,3): Keycode.P,
        (0,1,2,3): Keycode.U,

        # thumb (pin 4) combos (was pin 5 → now pin 4)
        (0,4): Keycode.M,  (1,4): Keycode.G,  (2,4): Keycode.H,
        (3,4): Keycode.B,

        (0,1,4): Keycode.Y,(0,2,4): Keycode.W,(0,3,4): Keycode.X,
        (1,2,4): Keycode.F,(1,3,4): Keycode.K,(2,3,4): Keycode.V,

        (0,1,2,4): Keycode.J,(1,2,3,4): Keycode.Z,
        (0,1,2,3,4): Keycode.Q
    },

    # ─── Layers 1–4: fill in your own maps ───
    {},  # layer 1
    {},  # layer 2
    {},  # layer 3
    {}   # layer 4
]

pending = None
COOLDOWN = 0.05

def check_chords():
    global layer, last_switch, pending

    now = time.monotonic()

    # Read pins into pressed[]
    for pin, idx in pin_to_idx.items():
        pressed[idx] = not pins[pin].value  # True when pressed

    # 1) If only thumb (pin 4) is pressed, cycle layer
    if pressed[4] and not any(pressed[:4]):
        if now - last_switch > SWITCH_DEBOUNCE:
            layer = (layer + 1) % NUM_LAYERS
            print(f"Switched to layer {layer}")
            last_switch = now
            pending = None
        return

    # 2) Build finger-key combo (ignore pin 4)
    combo = tuple(i for i in range(4) if pressed[i])

    if combo:
        # new chord
        if combo != pending:
            key = layer_maps[layer].get(combo)
            if key:
                kbd.press(key)
                kbd.release_all()
                pending = combo
                time.sleep(COOLDOWN)
    else:
        # all released → reset pending chord
        pending = None

# Main loop
while ble.connected:
    check_chords()
    time.sleep(0.01)
