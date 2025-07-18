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

DEBUG_L6 = True

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
SCROLL_REPEAT_MS  = 0.15   # or whatever interval you like
THUMB_HOLD_TO_LOCK = 0.12   # seconds you must hold thumb alone to trigger layer-lock

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
held_scroll_combo = ()
last_scroll       = 0.0
last_thumb_rise    = 0.0
thumb_locked       = False  # only lock once per hold

# ─── Mouse chords for layer-7 (no thumb) ─────────────────────────────
MOVE_DELTA = 5
ACCEL_MULTIPLIER = 2
ACCEL_CHORD = (1, 2, 3)  # three-finger accel combo

# ─── Core chord logic with layers 1–5 ──────────────────────────────

def check_chords():
    global layer, thumb_taps, last_tap_time
    global last_combo, pending_combo, sent_release, skip_scag, scag_skip_combo
    global modifier_armed, held_modifier, last_time, last_repeat, accel_active
    global held_nav_combo, last_nav, held_combo, last_pending_combo
    global held_scroll_combo, last_scroll

    now     = time.monotonic()
    pressed = tuple(not p.value for p in pins)
    combo   = tuple(i for i, down in enumerate(pressed) if down)

    # ─── A) Pure-thumb release ⇒ layer-lock (always first) ─────────────
    if last_combo == (4,) and combo == ():
        # count the tap
        if now - last_tap_time < TAP_WINDOW:
            thumb_taps += 1
        else:
            thumb_taps = 1
        last_tap_time = now

        # clamp & switch layer
        layer = min(thumb_taps, 7)
        print(f"→ locked to layer-{layer}")

        # reset all combo state
        pending_combo     = None
        sent_release      = False
        skip_scag         = False
        modifier_armed    = False
        held_modifier     = None
        scag_skip_combo   = None
        held_scroll_combo = ()

        # clear last_combo so it won’t retrigger
        last_combo = combo   # combo is ()
        return

    # ─── B) Stabilize into pending_combo ─────────────────────────────────
    if combo != last_combo:
        last_time = now
        if last_combo == () and combo != ():
            pending_combo  = None
            sent_release   = False

    ms = STABLE_MS_ALPHA if layer == 1 else STABLE_MS_OTHER
    if combo and (now - last_time) >= ms and combo != pending_combo:
        pending_combo = combo

    pending_changed    = (pending_combo != last_pending_combo)
    last_pending_combo = pending_combo

    # ─── C) Fetch this layer’s map ──────────────────────────────────────
    lm = chords_config.layer_maps[layer]

    # ───  macOS media keys ─────────────────────────────────
    if layer == 6:
        if combo and combo != last_combo and combo in lm:
            code = lm[combo]
            print(f"[L6] sending {code!r} for {combo}")
            cc.send(code)
            sent_release = True
            time.sleep(DEBOUNCE_UP)
        # **do not return here**—let the final update of last_combo happen below

    # ─── Layer-4 SCAG “arm” ──────────────────────────────────────────
    if layer == 4 and not modifier_armed and pending_combo in chords_config.scag:
        held_modifier   = chords_config.scag[pending_combo]
        modifier_armed  = True
        scag_skip_combo = pending_combo
        skip_scag       = True
        pending_combo = None
        last_combo    = ()
        return

    # ─── Layer-5: Mouse with event-only debug ───────────────────────────
    if layer == 5:
        accel_active = (pending_combo == chords_config.ACCEL_CHORD)

        # BUTTON CLICK
        if pending_combo in chords_config.mouse_button_chords and pending_changed:
            mouse.click(chords_config.mouse_button_chords[pending_combo])
            held_combo   = ()
            sent_release = True
            time.sleep(DEBOUNCE_UP)
            return

        # ─── SCROLL (initial & arm for repeat) ─────────────────────────────
        if pending_combo in chords_config.mouse_scroll_chords and pending_changed:
            amt = chords_config.mouse_scroll_chords[pending_combo]
            if accel_active:
                amt *= ACCEL_MULTIPLIER
            mouse.move(wheel=amt)
            held_scroll_combo = pending_combo
            last_scroll       = now
            sent_release      = True
            return

        # ─── SCROLL REPEAT ─────────────────────────────────────────────────
        if (
            pending_combo == held_scroll_combo
            and pending_combo in chords_config.mouse_scroll_chords
            and (now - last_scroll) >= SCROLL_REPEAT_MS
        ):
            amt = chords_config.mouse_scroll_chords[pending_combo]
            if accel_active:
                amt *= ACCEL_MULTIPLIER
            mouse.move(wheel=amt)
            last_scroll = now
            return

        # MOVE (initial)
        if pending_combo in chords_config.mouse_move_chords and pending_changed:
            dx, dy = chords_config.mouse_move_chords[pending_combo]
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            held_combo   = pending_combo
            last_repeat  = now
            sent_release = True
            return

        # MOVE REPEAT
        if pending_combo == held_combo \
           and pending_combo in chords_config.mouse_move_chords \
           and (now - last_repeat) >= L5_REPEAT_MS:
            dx, dy = chords_config.mouse_move_chords[held_combo]
            if accel_active:
                dx *= ACCEL_MULTIPLIER
                dy *= ACCEL_MULTIPLIER
            mouse.move(dx, dy)
            last_repeat = now
            return

        # HOLD
        if pending_combo in chords_config.mouse_hold_chords and pending_changed:
            mouse.press(chords_config.mouse_hold_chords[pending_combo])
            held_combo   = ()
            sent_release = True
            return

        # RELEASE
        if pending_combo in chords_config.mouse_release_chords and pending_changed:
            mouse.release(chords_config.mouse_release_chords[pending_combo])
            held_combo   = ()
            sent_release = True
            return

    # ─── First-release send for layers 1–3,6-7 ───────────────────────
    if len(combo) < len(last_combo) and last_combo and not sent_release:
        # skip SCAG if it’s the skip combo
        if skip_scag and last_combo == scag_skip_combo:
            skip_scag = False
        else:
            skip_layer_lock = True
            use = pending_combo or last_combo
            # SCAG send (layer-4)
            if layer == 4 and modifier_armed and last_combo in chords_config.alpha:
                key = chords_config.alpha[last_combo]
                keyboard.press(held_modifier, key)
                keyboard.release_all()
                layer       = 1
                thumb_taps  = 1
                modifier_armed = False
                skip_scag      = False
            # normal layers
            elif layer in (1, 2, 3, 6, 7):
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
