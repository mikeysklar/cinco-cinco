# cinco-cinco
Cinco Cinco

A 5-Key Chording Keyboard with Layered Input and BLE Support

Cinco Cinco is a compact, chording keyboard that uses just five low-profile keys to emulate a full keyboard. By combining keypresses into chords and utilizing five layers, Cinco Cinco enables efficient one-handed typing. With BLE support and a modular design, it’s ideal for mobile computing, minimal setups, and assistive technology use.

Table of Contents
    •   Features
    •   Why Chording?
    •   Hardware Highlights
    •   Design Files & Software Versions
    •   CircuitPython Compatibility
    •   Layer Maps
    •   Layer 1: Letters
    •   Layer 2: Numbers
    •   Layer 3: Whitespace & Delimiters
    •   Layer 4: Modifiers & Navigation
    •   Layer 5: Mouse Control / Media
    •   Typing Speed & Ergonomics

⸻

Features
    •   5-Key Chording Input: Access a complete keyboard with only 5 keys using layered chords.
    •   Wireless BLE Support: Includes a CircuitPython BLE HID example for wireless connectivity.
    •   Compact, Flat Design: Designed for portability and efficiency.
    •   No Finger Travel: All keys are always under your fingers, minimizing movement.
    •   STEMMA QT I2C Port: Supports a wide range of microcontrollers and displays.
    •   Single PCB, No Wiring: Keys are directly mounted — no matrix, no mess.

⸻

Why Chording?

Computing is rapidly changing. We are moving away from sitting at desks and staring at screens. Smart glasses and watches let us consume information on the go. Phones, which have taken too much of our attention, no longer need to be our primary method of communication.

The key is the keys.

With Cinco Cinco, we take advantage of our five fingers to create a new kind of keyboard — one that allows you to input text without finger travel, without looking, and in some cases without even needing your hands.

Chording opens up a future of input that is compact, discreet, and mobile. This same keyboard can also enhance desktop productivity, allowing CAD users and creatives to use one hand for keyboard shortcuts while the other handles precise mouse movements.

⸻

Hardware Highlights
    •   I2C STEMMA QT connector for easy expansion (displays, sensors)
    •   BLE-compatible controllers: Tested with nRF52840 and ESP32-S3 boards
    •   OLED/TFT support via I2C for live display of chords or active layers
    •   Low-profile tactile switches on a minimalist PCB layout

⸻

Design Files & Software Versions
    •   KiCad: Version 9
    •   FreeCAD: Version 1.x
    •   3D printable case files (coming soon)

All design files are open source and located in the pcb/ and case/ folders of this repository.

⸻

CircuitPython Compatibility
    •   Tested with CircuitPython: Version 9.2.8
    •   Includes support for adafruit_hid, adafruit_ble, and keypad

Sample code is provided in the circuitpython/ folder.

⸻

Layer Maps

Each layer uses unique key combinations (chords) to represent characters or commands. Key positions are numbered 0–4.

Layer 1: Letters

Standard QWERTY-style layout

(0,): a   (1,): e   (2,): i   (3,): o   (4,): u
(0,1): b  (0,2): c  ...

Layer 2: Numbers

0–9 and basic math symbols

(0,): 1   (1,): 2   (2,): 3   (3,): 4   (4,): 5
(0,1): 6  (0,2): 7  (1,2): 8  (1,3): 9  (0,4): 0

Layer 3: Whitespace & Delimiters

Tab, Enter, punctuation, brackets, etc.

(1,): TAB        (2,): .        (3,): -
(2,3): /         (0,1): ENTER   (0,2): ,
(1,3): [         (0,3): ]       (1,2,3): \
(1,2): BACKSPACE (0,1,3): '     (0,2,3): ;
(0,1,2,3): `

Layer 4: Modifiers & Navigation

Shift, Ctrl, Alt, arrow keys

(0,): SHIFT      (1,): CTRL     (2,): ALT
(3,): LEFT       (4,): RIGHT
(0,1): UP        (1,2): DOWN

Layer 5: Mouse Control / Media

Mouse movement, clicks, volume control

(0,): MOUSE_LEFT     (1,): MOUSE_RIGHT
(2,): VOLUME_UP      (3,): VOLUME_DOWN
(0,1): MOUSE_MOVE_X+ (0,2): MOUSE_MOVE_Y+


⸻

Typing Speed & Ergonomics

Cinco Cinco allows for:
    •   Faster typing with reduced finger travel
    •   One-handed operation while using a mouse
    •   Improved comfort and reduced strain

Skilled users report achieving 30–50 WPM within a few hours of practice. With dedicated layers and an intuitive chord map, long-term typing performance can rival traditional layouts — with fewer keys.

⸻

License

This project is licensed under the MIT License. All hardware and software files are open source.
