# Cinco-Cinco
*A 5-Key Chording Keyboard with Layered Input and BLE Support*

Cinco-Cinco is a compact, low-profile chording keyboard that uses just **five keys** to emulate a full keyboard. By combining keypresses into chords and utilizing **five software layers**, Cinco-Cinco enables efficient one-handed typing.  I had been building 7-key chording keyboards, but that reuires the hand to lose its home position and travel. Five keys and layers not only allows for all keys, but also all total control. It is a lot of fun to use.

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
- **BLE-compatible microcontrollers**: Tested with nRF52840
- **Optional OLED/TFT display** for live chord/layer feedback
- **All components on a single PCB** – no diodes, no hand wiring, just plug and go

---

## Design Files & Software Versions

### PCB & Schematic Files
- **KiCad**: Version 9

**Cinco-Cinco board (`cinco-cinco/` folder):**
- [`cinco-cinco.kicad_sch`](cinco-cinco/cinco-cinco.kicad_sch)
- [`cinco-cinco.kicad_pcb`](cinco-cinco/cinco-cinco.kicad_pcb)

**nnv2-smd board (`nnv2-smd/` folder):**
- [`nnv2-smd.kicad_sch`](nnv2-smd/nnv2-smd.kicad_sch)
- [`nnv2-smd.kicad_pcb`](nnv2-smd/nnv2-smd.kicad_pcb)

### Case Files (`cad/` folder)
- **FreeCAD**: Version 1.x
- [`case.FCStd`](cad/case.FCStd)

**STL files for 3D printing:**
- [`case-top-cvr.stl`](cad/case-top-cvr.stl)
- [`case-mid-cvr.stl`](cad/case-mid-cvr.stl)
- [`case-lwr-cvr.stl`](cad/case-lwr-cvr.stl)

**STEP files for 3D viewing:**
- [`case-top-cvr.step`](cad/case-top-cvr.step)
- [`case-mid-cvr.step`](cad/case-mid-cvr.step)
- [`case-lwr-cvr.step`](cad/case-lwr-cvr.step)
- [`case-cinco-cinco.step`](cad/case-cinco-cinco.step)
- [`case-bat1200.step`](cad/case-bat1200.step)
- [`case-nnv2-smd.step`](cad/case-nnv2-smd.step)


All hardware design files are open source and located in the `pcb/` and `cad/` directories of this repository.

---

## CircuitPython Compatibility

- **Tested with CircuitPython**: Version 9.2.8
- Library installation process if MacOS is used (delete the ._ libs)

```
circup install adafruit_ble adafruit_bus_device adafruit_hid
cd /Volumes/CIRCUITPY
find . -type f -name '._*' -delete

circup install adafruit_displayio_ssd1306 adafruit_display_text adafruit_ssd1306 adafruit_mcp230xx

cd /Volumes/CIRCUITPY
find . -type f -name '._*' -delete
```

---

## Layer Maps

Each layer uses unique key combinations (chords) from the 5 keys (positions 0–4).

| Finger | Key Index |
|:-------|:----------|
| Thumb  | 4         |
| Pinky  | 3         |
| Ring   | 2         |
| Middle | 1         |
| Fore   | 0         |

### Layer 1: Letters

## Layer 1: Letters (Compact Format)

## Layer 1: Letters (Reordered Columns)

| Key         | Pky | Rng | Mid | Idx | Thm | Chord         |
|-------------|:---:|:---:|:---:|:---:|:---:|---------------|
| A           |     |  x  |     |     |     | (2,)          |
| B           |  x  |     |     |     |  x  | (3,4)         |
| C           |  x  |     |     |  x  |     | (0,3)         |
| D           |     |  x  |  x  |  x  |     | (0,1,2)       |
| E           |     |     |     |  x  |     | (0,)          |
| F           |     |  x  |  x  |     |  x  | (1,2,4)       |
| G           |     |     |  x  |     |  x  | (1,4)         |
| H           |     |  x  |     |     |  x  | (2,4)         |
| I           |     |     |  x  |     |     | (1,)          |
| J           |     |  x  |  x  |  x  |  x  | (0,1,2,4)     |
| K           |  x  |     |  x  |     |  x  | (1,3,4)       |
| L           |  x  |     |  x  |     |     | (1,3)         |
| M           |     |     |     |  x  |  x  | (0,4)         |
| N           |     |  x  |  x  |     |     | (1,2)         |
| O           |     |  x  |     |  x  |     | (0,2)         |
| P           |  x  |  x  |  x  |     |     | (1,2,3)       |
| Q           |  x  |  x  |  x  |  x  |  x  | (0,1,2,3,4)   |
| R           |     |     |  x  |  x  |     | (0,1)         |
| S           |     |     |     |     |  x  | (3,)          |
| T           |  x  |  x  |     |     |     | (2,3)         |
| U           |  x  |  x  |  x  |  x  |     | (0,1,2,3)     |
| V           |  x  |  x  |     |     |  x  | (2,3,4)       |
| W           |     |  x  |     |  x  |  x  | (0,2,4)       |
| X           |  x  |     |     |  x  |  x  | (0,3,4)       |
| Y           |     |     |  x  |  x  |  x  | (0,1,4)       |
| Z           |  x  |  x  |  x  |     |  x  | (1,2,3,4)     |
| BACKSPACE   |  x  |     |  x  |  x  |     | (0,1,3)       |
| SPACE       |  x  |  x  |     |  x  |     | (0,2,3)       |
    
## Layer 2: Numbers and Arrows (Compact Format)

| Key         | Pky | Rng | Mid | Idx | Thm | Chord         |
|-------------|:---:|:---:|:---:|:---:|:---:|---------------|
| 1           |     |     |     |  x  |     | (0,)          |
| 2           |     |     |  x  |     |     | (1,)          |
| 3           |     |  x  |     |     |     | (2,)          |
| 4           |  x  |     |     |     |     | (3,)          |
| 5           |     |     |  x  |  x  |     | (0,1)         |
| 6           |     |  x  |  x  |     |     | (1,2)         |
| 7           |  x  |  x  |     |     |     | (2,3)         |
| 8           |     |  x  |     |  x  |     | (0,2)         |
| 9           |  x  |     |  x  |     |     | (1,3)         |
| 0           |     |  x  |  x  |  x  |     | (0,1,2)       |
| ↑ (Up)      |  x  |     |     |  x  |     | (0,3)         |
| ↓ (Down)    |  x  |  x  |  x  |     |     | (1,2,3)       |
| → (Right)   |  x  |     |  x  |  x  |     | (0,1,3)       |
| ← (Left)    |  x  |  x  |     |  x  |     | (0,2,3)       |
| ESCAPE      |  x  |  x  |  x  |  x  |     | (0,1,2,3)     |

## Layer 3: Whitespace & Delimiters (Reordered Columns)

| Key            | Pky | Rng | Mid | Idx | Thm | Chord         |
|----------------|:---:|:---:|:---:|:---:|:---:|---------------|
| ESCAPE         |     |     |     |  x  |     | (0,)          |
| TAB            |     |     |  x  |     |     | (1,)          |
| PERIOD (.)     |     |  x  |     |     |     | (2,)          |
| MINUS (-)      |  x  |     |     |     |     | (3,)          |
| FORWARD_SLASH  |  x  |  x  |     |     |     | (2,3)         |
| ENTER          |     |     |  x  |  x  |     | (0,1)         |
| COMMA (,)      |     |  x  |     |  x  |     | (0,2)         |
| LEFT_BRACKET   |  x  |     |  x  |     |     | (1,3)         |
| RIGHT_BRACKET  |  x  |     |     |  x  |     | (0,3)         |
| BACKSLASH (\\) |  x  |  x  |  x  |     |     | (1,2,3)       |
| BACKSPACE      |     |  x  |  x  |     |     | (1,2)         |
| QUOTE (')      |  x  |     |  x  |  x  |     | (0,1,3)       |
| SEMICOLON (;)  |  x  |  x  |     |  x  |     | (0,2,3)       |
| GRAVE (`)      |  x  |  x  |  x  |  x  |     | (0,1,2,3)     |

## Layer 4: Modifiers & Navigation (SCAG)

| Key     | Pky | Rng | Mid | Idx | Thm | Chord     |
|---------|:---:|:---:|:---:|:---:|:---:|-----------|
| SHIFT   |  x  |     |     |     |     | (3,)      |
| CTRL    |     |  x  |     |     |     | (2,)      |
| ALT     |     |     |  x  |     |     | (1,)      |
| GUI     |     |     |     |  x  |     | (0,)      |

## Layer 5: Mouse Control (Movement, Scroll, Buttons)

| Action           | Pky | Rng | Mid | Idx | Thm | Chord       |
|------------------|:---:|:---:|:---:|:---:|:---:|-------------|
| **MOVE LEFT**      |     |     |     |  x  |     | `(0,)`        |
| **MOVE RIGHT**     |     |     |  x  |     |     | `(1,)`        |
| **MOVE UP**        |     |  x  |     |     |     | `(2,)`        |
| **MOVE DOWN**      |  x  |     |     |     |     | `(3,)`        |
| **SCROLL UP**      |  x  |     |     |  x  |     | `(0,3)`       |
| **SCROLL DOWN**    |  x  |     |     |     |  x  | `(3,4)`       |
| **LEFT CLICK**     |     |     |  x  |  x  |     | `(0,1)`       |
| **RIGHT CLICK**    |  x  |     |     |  x  |     | `(2,3)`       |
| **MIDDLE CLICK**   |     |  x  |  x  |     |     | `(1,2)`       |
| **BACK BUTTON**    |     |     |     |  x  |  x  | `(0,4)`       |
| **FORWARD BUTTON** |  x  |     |     |     |  x  | `(3,4)`       |
| **HOLD LEFT**      |     |  x  |  x  |     |  x  | `(0,1,4)`     |
| **RELEASE LEFT**   |     |     |  x  |  x  |  x  | `(1,2,4)`     |
| **ACCELERATE**     |     |  x  |     |     |  x  | `(2,4)`       |
