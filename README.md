# Cinco-Cinco
*A 5-Key Chording Keyboard with Layered Input and BLE Support*

Cinco-Cinco is a compact, flat-profile chording keyboard that uses just **five low-profile keys** to emulate a full keyboard. By combining keypresses into chords and utilizing **five software layers**, Cinco-Cinco enables efficient one-handed typing. With optional BLE support and a modular design, it's ideal for mobile computing, minimal setups, and assistive technology use.

## Table of Contents
- [Features](#features)
- [Why Chording?](#why-chording)
- [Hardware Highlights](#hardware-highlights)
- [Design Files & Software Versions](#design-files--software-versions)
- [CircuitPython Compatibility](#circuitpython-compatibility)
- [Layer Maps](#layer-maps)
  - [Layer 1: Letters](#layer-1-letters)
  - [Layer 2: Numbers](#layer-2-numbers)
  - [Layer 3: Whitespace & Delimiters](#layer-3-whitespace--delimiters)
  - [Layer 4: Modifiers & Navigation](#layer-4-modifiers--navigation)
  - [Layer 5: Mouse Control / Media](#layer-5-mouse-control--media)
- [Typing Speed & Ergonomics](#typing-speed--ergonomics)
- [License](#license)

---

## Features

- **5-Key Chording Input** – Access a complete keyboard using just 5 keys across multiple layers
- **Wireless BLE Support** – Includes a CircuitPython BLE HID example for wireless connectivity
- **Compact, Flat Design** – Ideal for one-handed, mobile, or embedded use
- **No Finger Travel** – All inputs stay under your fingertips to reduce movement and increase speed
- **STEMMA QT I2C Port** – Compatible with a variety of microcontrollers and displays
- **Single PCB, No Wiring** – Low-profile switches soldered directly to the board for minimal complexity

---

## Why Chording?

Computing is rapidly changing. We are moving away from sitting at desks and staring at screens. Smart glasses and watches let us consume information on the go. Phones, which have taken too much of our attention, no longer need to be our primary method of communication.

**The key is the keys.**

With Cinco-Cinco, we take advantage of our five fingers to create a new kind of keyboard — one that allows you to input text **without finger travel**, without looking, and in some cases **without even needing your hands**.

Chording opens up a future of input that is compact, discreet, and mobile. This same keyboard can also enhance desktop productivity, allowing CAD users and creatives to use one hand for keyboard shortcuts while the other handles precise mouse movements.

---

## Hardware Highlights

- **I2C STEMMA QT connector** for plug-and-play support with sensors and displays
- **BLE-compatible microcontrollers**: Tested with Adafruit nRF52840, ESP32-S3
- **Optional OLED/TFT display** for live chord/layer feedback
- **All components on a single PCB** – no diodes, no hand wiring, just plug and go

---

## Design Files & Software Versions

- **KiCad**: Version 9
- **FreeCAD**: Version 1.x
- **3D printable case**: Coming soon

All hardware files are open source and available in the `pcb/` and `case/` directories.

---

## CircuitPython Compatibility

- **Tested with CircuitPython**: Version 9.2.8
- Requires `adafruit_hid`, `adafruit_ble`, `keypad`, and standard BLE libraries
- BLE HID keyboard example included in `circuitpython/` folder

---

## Layer Maps

Each layer uses unique key combinations (chords) from the 5 keys (positions 0–4).

### Layer 1: Letters
*Standard QWERTY-style letter mapping*
