# chords_config.py
# All chord mappings for c5k-left.py, grouped by layer.

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# ────────────── Layer 1: Alpha ──────────────
layer1_chords = {  # layer-1: alpha
    (0,):           Keycode.E,
    (1,):           Keycode.I,
    (2,):           Keycode.A,
    (3,):           Keycode.S,
    (0, 1):         Keycode.R,
    (0, 2):         Keycode.O,
    (0, 3):         Keycode.C,
    (1, 2):         Keycode.N,
    (1, 3):         Keycode.L,
    (2, 3):         Keycode.T,
    (0, 1, 2):      Keycode.D,
    (1, 2, 3):      Keycode.P,
    (0, 1, 2, 3):   Keycode.U,
    (0, 2, 3):      Keycode.SPACE,
    (0, 1, 3):      Keycode.BACKSPACE,
    (0, 4):         Keycode.M,
    (1, 4):         Keycode.G,
    (2, 4):         Keycode.H,
    (3, 4):         Keycode.B,
    (0, 1, 4):      Keycode.Y,
    (0, 2, 4):      Keycode.W,
    (0, 3, 4):      Keycode.X,
    (1, 2, 4):      Keycode.F,
    (1, 3, 4):      Keycode.K,
    (2, 3, 4):      Keycode.V,
    (0, 1, 2, 4):   Keycode.J,
    (1, 2, 3, 4):   Keycode.Z,
    (0, 1, 2, 3, 4):Keycode.Q,
}

# ────────────── Layer 2: Numbers & Arrows ──────────────
layer2_chords = {  # layer-2: numbers & thumb-based arrows
    # Numbers (unchanged)
    (0,):           Keycode.ONE,
    (1,):           Keycode.TWO,
    (2,):           Keycode.THREE,
    (3,):           Keycode.FOUR,
    (0, 1):         Keycode.FIVE,
    (1, 2):         Keycode.SIX,
    (2, 3):         Keycode.SEVEN,
    (0, 2):         Keycode.EIGHT,
    (1, 3):         Keycode.NINE,
    (0, 1, 2):      Keycode.ZERO,

    # Thumb-based ARROWS 
    (0, 4):         Keycode.UP_ARROW,
    (1, 4):         Keycode.DOWN_ARROW,
    (2, 4):         Keycode.RIGHT_ARROW,
    (3, 4):         Keycode.LEFT_ARROW,

    # Thumb-based NAV
    (0, 1, 4):      Keycode.PAGE_UP,
    (2, 3, 4):      Keycode.PAGE_DOWN,
    (0, 1, 2, 4):   Keycode.END,
    (0, 2, 4):      Keycode.DELETE,
    (1, 3, 4):      Keycode.INSERT,
    (1, 2, 3, 4):   Keycode.HOME,
}

# ────────────── Layer 3: Whitespace & Delimiters ──────────────
layer3_chords = {  # layer-3: whitespace & delimiters
    (0,):           Keycode.ESCAPE,
    (1,):           Keycode.TAB,
    (2,):           Keycode.PERIOD,
    (3,):           Keycode.MINUS,
    (2, 3):         Keycode.FORWARD_SLASH,
    (0, 1):         Keycode.ENTER,
    (0, 2):         Keycode.COMMA,
    (1, 3):         Keycode.LEFT_BRACKET,
    (0, 3):         Keycode.RIGHT_BRACKET,
    (1, 2, 3):      Keycode.BACKSLASH,
    (1, 2):         Keycode.BACKSPACE,
    (0, 1, 3):      Keycode.QUOTE,
    (0, 2, 3):      Keycode.SEMICOLON,
    (0, 1, 2, 3):   Keycode.GRAVE_ACCENT,
    (0, 1, 2):      Keycode.DELETE,
}

# ────────────── Layer 4: Modifiers ──────────────
modifier_chords = {
    (3,):       Keycode.LEFT_SHIFT,
    (2,):       Keycode.LEFT_CONTROL,
    (1,):       Keycode.LEFT_ALT,
    (0,):       Keycode.LEFT_GUI,      # CMD / WIN
    (0, 1):     Keycode.RIGHT_ALT,     # OPTION (⌥)
}

# ────────────── Layer 5: Navigation ──────────────
layer5_chords = {   # 5: web navigation layer

    # Directional browsing (same orientation as arrows in Layer-2)
    (0, 4):         Keycode.PAGE_UP,                         # Up → PgUp
    (1, 4):         Keycode.PAGE_DOWN,                       # Down → PgDn
    (2, 4):         (Keycode.SHIFT, Keycode.BACKSPACE),      # Right → Forward
    (3, 4):         Keycode.BACKSPACE,                       # Left → Back

    # Tab & window management
    (0, 1):         (Keycode.CONTROL, Keycode.T),            # New Tab
    (1, 2):         (Keycode.CONTROL, Keycode.W),            # Close Tab
    (2, 3):         (Keycode.CONTROL, Keycode.SHIFT, Keycode.T),  # Reopen Closed Tab
    (0, 2):         (Keycode.CONTROL, Keycode.N),            # New Window
    (1, 3):         (Keycode.CONTROL, Keycode.SHIFT, Keycode.W),  # Close Window

    # Page utilities
    (0, 1, 4):      (Keycode.CONTROL, Keycode.R),            # Refresh
    (1, 2, 4):      (Keycode.CONTROL, Keycode.SHIFT, Keycode.R),  # Hard Refresh
    (2, 3, 4):      (Keycode.CONTROL, Keycode.L),            # Focus Address Bar
    (0, 3):         (Keycode.CONTROL, Keycode.F),            # Find on Page
    (0, 2, 3):      (Keycode.CONTROL, Keycode.H),            # History
    (1, 2, 3):      (Keycode.CONTROL, Keycode.J),            # Download
}

# ────────────── Layer 6: macOS Media Keys ──────────────
layer6_chords = {   # 6: macOS media keys
    (0,):           ConsumerControlCode.BRIGHTNESS_DECREMENT,
    (1,):           ConsumerControlCode.BRIGHTNESS_INCREMENT,
    (2,):           ConsumerControlCode.VOLUME_DECREMENT,
    (3,):           ConsumerControlCode.VOLUME_INCREMENT,
    (0, 1):         ConsumerControlCode.MUTE,
    (2, 3):         ConsumerControlCode.PLAY_PAUSE,
    (0, 2):         ConsumerControlCode.SCAN_NEXT_TRACK,
    (1, 3):         ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    (0, 3):         ConsumerControlCode.FAST_FORWARD,
    (1, 2):         ConsumerControlCode.REWIND,
    (0, 1, 2):      ConsumerControlCode.STOP,
    (0, 1, 3):      ConsumerControlCode.EJECT,
}

# ────────────── Layer 7: Mouse Actions ──────────────
# Mouse move chords: chord → (dx, dy)
mouse_move_chords = {
    (1, 3):   (-1,  0),  # Move Left
    (1, 2):   ( 0,  1),  # Move Up
    (2, 3):   ( 1,  0),  # Move Right
    (0, 3):   ( 0, -1),  # Move Down
}
# Mouse button chords: chord → Mouse button
mouse_button_chords = {
    (0, 3):   Mouse.LEFT_BUTTON,
    (1, 2):   Mouse.RIGHT_BUTTON,
    (1, 3):   Mouse.MIDDLE_BUTTON,
    (2, 3):   Mouse.FORWARD_BUTTON,
}
# Mouse scroll chords: chord → scroll direction
mouse_scroll_chords = {
    (2, 3):      1,    # Scroll Up
    (0, 2, 3):  -1,    # Scroll Down
}
# Mouse hold chords: chord → Mouse button
mouse_hold_chords = {
    (0, 1, 2): Mouse.LEFT_BUTTON,  # Hold Left Button
}
# Mouse release chords: chord → Mouse button
mouse_release_chords = {
    (0, 1, 3): Mouse.LEFT_BUTTON,  # Release Left Button
}
# Chord for acceleration (if you use one)
ACCEL_CHORD = (1, 2, 3)

# ────────────── Layer 8: (Duplicate of Layer 6 for completeness) ──────────────
layer8_chords = {   # 8: function keys F1–F12
    (0,):           Keycode.F1,
    (1,):           Keycode.F2,
    (2,):           Keycode.F3,
    (3,):           Keycode.F4,
    (0, 1):         Keycode.F5,
    (0, 2):         Keycode.F6,
    (0, 3):         Keycode.F7,
    (1, 2):         Keycode.F8,
    (1, 3):         Keycode.F9,
    (2, 3):         Keycode.F10,
    (0, 1, 2):      Keycode.F11,
    (0, 1, 3):      Keycode.F12,
}

# ────────────── Central Layer Map ──────────────
layer_maps = {
    1: layer1_chords,
    2: layer2_chords,
    3: layer3_chords,
    4: modifier_chords,
    5: layer5_chords,
    6: layer6_chords,
    7: {   # Mouse layer bundle
        "move":    mouse_move_chords,
        "button":  mouse_button_chords,
        "scroll":  mouse_scroll_chords,
        "hold":    mouse_hold_chords,
        "release": mouse_release_chords,
        "accel":   ACCEL_CHORD,
    },
    8: layer8_chords,
}
