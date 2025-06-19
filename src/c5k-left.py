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
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import chords_config

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
cc = ConsumerControl(hid_svc.devices)
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
NAV_REPEAT_MS    = 0.2   # min seconds between repeats on layer-5 nav
LAYER_LOCK_COOLDOWN = 0.1  # minimum seconds between layer‐lock taps

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
held_nav_combo   = ()
last_nav         = 0.0
last_pending_combo = None
last_layer_change = 0.0
skip_layer_lock = False

# ─── Chord maps ──────────────────────────────

def get_chord_mapping(layer):
    return {
        1: layer1_chords,
        2: layer2_chords,
        3: layer3_chords,
        4: modifier_chords,
        5: layer5_chords,
        6: layer6_chords,
        7: {  # Mouse
            "move": mouse_move_chords,
            "button": mouse_button_chords,
            "scroll": mouse_scroll_chords,
            "hold": mouse_hold_chords,
            "release": mouse_release_chords,
            "accel": ACCEL_CHORD,
        },
        8: layer8_chords,
    }[layer]

# ─── Mouse chords for layer-7 (no thumb) ─────────────────────────────
MOVE_DELTA = 5
ACCEL_MULTIPLIER = 2
ACCEL_CHORD = (1, 2, 3)  # three-finger accel combo

# ─── Core chord logic with layers 1–5 ──────────────────────────────

def check_chords():
    global layer, thumb_taps, tap_in_prog, last_tap_time
    global last_combo, pending_combo, sent_release, skip_scag, scag_skip_combo
    global modifier_armed, held_modifier, last_time, last_repeat, accel_active
    global held_nav_combo, last_nav, held_combo, last_pending_combo, last_layer_change
    global skip_layer_lock

    now = time.monotonic()
    # Read all 5 pins (0–3 fingers, 4 thumb)
    pressed = tuple(not p.value for p in pins)

    # ─── 1) Build & stabilize combo (pending_combo) ────────────────────
    combo = tuple(i for i, down in enumerate(pressed) if down)
    if combo != last_combo:
        last_time = now
        if last_combo == () and combo != ():
            pending_combo = None
            sent_release   = False
    ms = STABLE_MS_ALPHA if layer == 1 else STABLE_MS_OTHER
    if combo and (now - last_time) >= ms and combo != pending_combo:
        pending_combo = combo
    pending_changed = (pending_combo != last_pending_combo)
    last_pending_combo = pending_combo

    # ─── 2) Pure-thumb tap ⇒ lock layers (only when pending_combo==(4,)) ─
    if (
        not skip_layer_lock
        and pending_combo == (4,)
        and pending_changed
        and (now - last_layer_change) >= LAYER_LOCK_COOLDOWN
    ):
        # record when we changed
        last_layer_change = now

        # then your existing lock logic:
        tap_in_prog = True
        if now - last_tap_time < TAP_WINDOW:
            thumb_taps += 1
        else:
            thumb_taps = 1
        last_tap_time = now
        layer = min(thumb_taps, 8)
        print(f"→ locked to layer-{layer}")

        # reset combo state
        last_combo      = ()
        pending_combo   = None
        sent_release    = False
        skip_scag       = False
        modifier_armed  = False
        held_modifier   = None
        scag_skip_combo = None
        skip_layer_lock = False 
        return

    # allow next pure-thumb once you lift off
    if pending_combo != (4,):
        tap_in_prog = False

    # Grab this layer’s mapping
    lm = chords_config.layer_maps[layer]

    # ─── 6) Layer-4 SCAG “arm” ──────────────────────────────────────────
    if layer == 4 and not modifier_armed and pending_combo in chords_config.modifier_chords:
        held_modifier   = chords_config.modifier_chords[pending_combo]
        modifier_armed  = True
        scag_skip_combo = pending_combo
        skip_scag       = True
        print(f"→ modifier armed: {held_modifier}")
        pending_combo = None
        last_combo    = ()
        return

    # ─── 5) Layer-5: Mouse (move, click, scroll, hold/release) ─────────
    if layer == 5:
        accel_active = (pending_combo == chords_config.ACCEL_CHORD)

        # buttons
        if pending_combo in chords_config.mouse_button_chords:
            mouse.click(chords_config.mouse_button_chords[pending_combo])
            sent_release = True
            time.sleep(DEBOUNCE_UP)
            return

        # scroll
        if pending_combo in chords_config.mouse_scroll_chords:
            amt = chords_config.mouse_scroll_chords[pending_combo]
            if accel_active:
                amt *= ACCEL_MULTIPLIER
            mouse.move(wheel=amt)
            sent_release = True
            time.sleep(DEBOUNCE_UP)
            return

        # move
        if pending_combo in chords_config.mouse_move_chords:
            dx, dy = chords_config.mouse_move_chords[pending_combo]
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            held_combo  = pending_combo
            last_repeat = now
            sent_release = True
            return

        # repeat move
        if pending_combo == held_combo and (now - last_repeat) >= L5_REPEAT_MS:
            dx, dy = chords_config.mouse_move_chords[held_combo]
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            last_repeat = now
            return

        # hold & release
        if pending_combo in chords_config.mouse_hold_chords:
            mouse.press(chords_config.mouse_hold_chords[pending_combo])
            sent_release = True
            return
        if pending_combo in chords_config.mouse_release_chords:
            mouse.release(chords_config.mouse_release_chords[pending_combo])
            sent_release = True
            return

    # ─── 4) Layer-6: macOS media keys ─────────────────────────────────
    if layer == 6 and pending_combo in lm:
        print(f"→ media L6 combo {pending_combo} → {lm[pending_combo]!r}")
        cc.send(lm[pending_combo])
        sent_release = True
        time.sleep(DEBOUNCE_UP)
        return

    # ─── 7) First-release send for layers 1–4,6,8 ───────────────────────
    if len(combo) < len(last_combo) and last_combo and not sent_release:
        # skip SCAG if it’s the skip combo
        if skip_scag and last_combo == scag_skip_combo:
            skip_scag = False
        else:
            skip_layer_lock = True
            use = pending_combo or last_combo
            # SCAG send (layer-4)
            if layer == 4 and modifier_armed and last_combo in chords_config.layer1_chords:
                key = chords_config.layer1_chords[last_combo]
                keyboard.press(held_modifier, key)
                keyboard.release_all()
                print(f"→ sent {held_modifier}+{key}")
                layer       = 1
                thumb_taps  = 1
                modifier_armed = False
                skip_scag      = False
            # normal layers
            elif layer in (1, 2, 3, 6, 8):
                if use != (4,):  # ignore pure thumb
                    kc = lm.get(use)
                    if kc:
                        keyboard.press(kc)
                        keyboard.release_all()
                    else:
                        print(f"Unknown L{layer}: {use!r}")
        sent_release = True
        time.sleep(DEBOUNCE_UP)

    # ─── 8) Clear on full release ────────────────────────────────────────
    if not combo and last_combo:
        pending_combo  = None
        sent_release   = False
        held_nav_combo = ()
        skip_layer_lock = False

    # Save for next pass
    last_combo = combo

# ─── Main loop ────────────────────────────────────────────────
while ble.connected:
    check_chords()
    time.sleep(0.01)
