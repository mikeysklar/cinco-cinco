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

# ─── Hardware setup ────────────────────────────────────────────────────
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

# ─── BLE HID setup ────────────────────────────────────────────────────
ble = adafruit_ble.BLERadio()
hid_svc = HIDService()
advert = ProvideServicesAdvertisement(hid_svc)
keyboard = Keyboard(hid_svc.devices)
mouse = Mouse(hid_svc.devices)
ble.start_advertising(advert)
while not ble.connected:
    pass
ble.stop_advertising()

# ─── Timing constants ────────────────────────────────────────────────
STABLE_MS_ALPHA = 0.03   # 30 ms for layer-1 (alpha)
STABLE_MS_OTHER = 0.02   # 20 ms for layers 2/3
DEBOUNCE_UP      = 0.05  # pause after send
TAP_WINDOW       = 0.5   # thumb-tap window
MIN_TAP_INT      = 0.1   # thumb debounce
L5_REPEAT_MS     = 0.1   # repeat interval for held moves

# ─── State variables ────────────────────────────────────────────────
layer            = 1     # layers 1..5
thumb_taps       = 0
tap_in_prog      = False
last_tap_time    = 0.0
last_combo       = ()
pending_combo    = None
sent_release     = False
skip_scag        = False
scag_skip_combo  = None
modifier_armed   = False
held_modifier    = None
last_time        = time.monotonic()
held_combo       = ()
last_repeat      = 0.0
accel_active     = False

# ─── SCAG modifier chords for layer-4 ───────────────────────────────
modifier_chords = {
    (3,): Keycode.LEFT_SHIFT,
    (2,): Keycode.LEFT_CONTROL,
    (1,): Keycode.LEFT_ALT,
    (0,): Keycode.LEFT_GUI
}

# ─── Chord maps for layers 1–3; index 0 unused ──────────────────────────────
layer_maps = [
    {},
    { # layer-1: alpha
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
    },
    { # layer-3: whitespace & delimiters
      (0,):Keycode.ESCAPE,        (1,):Keycode.TAB,             (2,):Keycode.PERIOD,        (3,):Keycode.MINUS,
      (2,3):Keycode.FORWARD_SLASH,(0,1):Keycode.ENTER,          (0,2):Keycode.COMMA,        (1,3):Keycode.LEFT_BRACKET,
      (0,3):Keycode.RIGHT_BRACKET,(1,2,3):Keycode.BACKSLASH,    (1,2):Keycode.BACKSPACE,    (0,1,3):Keycode.QUOTE,
      (0,2,3):Keycode.SEMICOLON,  (0,1,2,3):Keycode.GRAVE_ACCENT,(0,1,2):Keycode.DELETE
    }
]

# ─── Mouse chords for layer-5 (no thumb) ─────────────────────────────
MOVE_DELTA = 5
ACCEL_MULTIPLIER = 2
ACCEL_CHORD = (1, 2, 3)  # three-finger accel combo

mouse_move_chords = {
    (0,): (-MOVE_DELTA,  0),   # ←
    (1,): ( MOVE_DELTA,  0),   # →
    (2,): (       0, -MOVE_DELTA),  # ↑
    (3,): (       0,  MOVE_DELTA),  # ↓
}

mouse_button_chords = {
    (0, 1): Mouse.LEFT_BUTTON,     # left click
    (0, 2): Mouse.RIGHT_BUTTON,    # right click
    (1, 2): Mouse.MIDDLE_BUTTON,   # middle click
    (0, 3): Mouse.BACK_BUTTON,     # back
    (1, 3): Mouse.FORWARD_BUTTON,  # forward
}

mouse_scroll_chords = {
    (2, 3):  1,    # scroll up
    (0, 2, 3): -1, # scroll down
}

mouse_hold_chords = {
    (0, 1, 2): Mouse.LEFT_BUTTON,  # press & hold left
}

mouse_release_chords = {
    (0, 1, 3): Mouse.LEFT_BUTTON,  # release left
}

# ─── Core chord logic with layers 1–5 ──────────────────────────────

def check_chords():
    global layer, thumb_taps, tap_in_prog, last_tap_time
    global last_combo, pending_combo, sent_release, skip_scag, scag_skip_combo
    global modifier_armed, held_modifier, last_time, held_combo, last_repeat, accel_active

    now = time.monotonic()
    pressed = tuple(not p.value for p in pins)
    finger = any(pressed[:4])
    thumb = pressed[4]

    # 1) thumb taps → lock layers 1–5
    if thumb and not finger and not tap_in_prog:
        tap_in_prog = True
        if now - last_tap_time < TAP_WINDOW:
            thumb_taps += 1
        else:
            thumb_taps = 1
        last_tap_time = now
        layer = min(thumb_taps, 5)
        print(f"→ locked to layer-{layer}")
        last_combo = ()
        pending_combo = None
        sent_release = False
        skip_scag = False
        modifier_armed = False
        held_modifier = None
        scag_skip_combo = None
        return
    if not thumb:
        tap_in_prog = False

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

    # 3) layer-5 mouse handling with held mode and acceleration
    if layer == 5:
        accel_active = (combo == ACCEL_CHORD)

        if combo in mouse_button_chords:
            mouse.click(mouse_button_chords[combo])
            sent_release = True
            time.sleep(DEBOUNCE_UP)
            return
        if combo in mouse_scroll_chords:
            scroll_amount = mouse_scroll_chords[combo]
            if accel_active:
                scroll_amount *= ACCEL_MULTIPLIER
            mouse.move(wheel=scroll_amount)
            sent_release = True
            time.sleep(DEBOUNCE_UP)
            return
        if combo in mouse_move_chords:
            dx, dy = mouse_move_chords[combo]
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            held_combo = combo
            last_repeat = now
            sent_release = True
            return
        if combo == held_combo and (now - last_repeat) >= L5_REPEAT_MS:
            dx, dy = mouse_move_chords.get(combo, (0, 0))
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            last_repeat = now
            return
        if combo != held_combo:
            held_combo = ()
        if combo in mouse_hold_chords:
            mouse.press(mouse_hold_chords[combo])
            sent_release = True
            return
        if combo in mouse_release_chords:
            mouse.release(mouse_release_chords[combo])
            sent_release = True
            return

    # 4) SCAG logic for layer-4
    if layer == 4 and not modifier_armed and pending_combo in modifier_chords:
        held_modifier = modifier_chords[pending_combo]
        modifier_armed = True
        scag_skip_combo = pending_combo
        skip_scag = True
        print(f"→ modifier armed: {held_modifier}")
        pending_combo = None
        last_combo = ()
        return

    # 5) first-release send for layers 1–4
    if len(combo) < len(last_combo) and last_combo and not sent_release:
        if skip_scag and last_combo == scag_skip_combo:
            skip_scag = False
        else:
            if layer == 4 and modifier_armed and last_combo in layer_maps[1]:
                key = layer_maps[1][last_combo]
                keyboard.press(held_modifier, key)
                keyboard.release_all()
                print(f"→ sent {held_modifier}+{key}")
                layer = 1
                thumb_taps = 1
                modifier_armed = False
                skip_scag = False
            elif layer in (1, 2, 3):
                use = pending_combo or last_combo
                if use != (4,):
                    kc = layer_maps[layer].get(use)
                    if kc:
                        keyboard.press(kc)
                        keyboard.release_all()
                    else:
                        print(f"Unknown L{layer}: {use}")
        sent_release = True
        time.sleep(DEBOUNCE_UP)

    # 6) clear on full release
    if combo == () and last_combo != ():
        pending_combo = None
        sent_release = False

    last_combo = combo

# ─── Main loop ────────────────────────────────────────────────
while ble.connected:
    check_chords()
    time.sleep(0.01)
