# Cinco-Cinco
*A 5-Key Chording Keyboard with Layered Input and BLE Support*

Cinco-Cinco is a wireless BLE, low-profile chording keyboard that uses just **five keys** to emulate a full keyboard. By combining keypresses into chords and utilizing **seven layers**, Cinco-Cinco enables efficient one-handed typing.  

I have spent the last year building pocket keybaords. My [BUBBY](https://github.com/mikeysklar/bubby) is a daily carry which I use for todos, lists and reminders. It made me enjoy typing with one hand to the point that I wanted a desktop version which has become the cinco-cinco. 

## Table of Contents
- [Why Chording?](#why-chording)
- [Hardware Highlights](#hardware-highlights)
- [CircuitPython Compatibility](#circuitpython-compatibility)
- [Design Files & Software Versions](#design-files--software-versions)
- [Layer Maps](#layer-maps)
  - [Layer 1: Letters](#layer-1-letters)
  - [Layer 2: Numbers](#layer-2-numbers)
  - [Layer 3: Whitespace & Delimiters](#layer-3-whitespace--delimiters)
  - [Layer 4: Modifiers & Navigation](#layer-4-modifiers--navigation)
  - [Layer 5: Mouse Control / Media](#layer-5-mouse-control--media)
  - [Layer 6: Media](#layer-6-media)
  - [Layer 7: F1 - F12](#layer-7-F1---F12)
- [Typing Speed](#typing-speed)
- [BOM](#bill-of-materials)
- [License](#license)

---

## Why Chording?

Computing is rapidly changing. We are moving away from sitting at desks and staring at screens. Smart glasses and watches let us consume information on the go. Phones, which have taken too much of our attention, no longer need to be our primary method of communication.

**The keys are key**

With Cinco-Cinco, we take advantage of our five fingers to create a new kind of keyboard — one that allows you to input text **without finger travel**, without looking, and in some cases **without even needing your hands**.

Chording opens up a future of input that is compact, discreet, and mobile. This same keyboard can also enhance desktop productivity, allowing CAD users and creatives to use one hand for keyboard shortcuts while the other handles precise mouse movements.

---

## Hardware Highlights

- **I2C STEMMA QT connector** for plug-and-play support for different controllers
- **BLE-compatible microcontrollers**: Tested with nRF52840
- **All components on a single PCB** – no diodes, no hand wiring, just plug and go
- **Two PCB system** - one controller board and one keypad
- **HW based key detection** - mcp23008, fast (400 kHz) for accurate chord detection
- **1200mAh Battery** - hold keypad in place and reduces charge frequency

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


## Layer Maps

Each layer uses unique key combinations (chords) from the 5 keys (positions 0–4).

| Finger | Key Index |
|:-------|:----------|
| Thumb  | 4         |
| Pinky  | 3         |
| Ring   | 2         |
| Middle | 1         |
| Fore   | 0         |

## Layer 1: Letters 

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
    
## Layer 2: Numbers and Arrows 

| Action      | Pky | Rng | Mid | Idx | Thm | Chord           |
|-------------|:---:|:---:|:---:|:---:|:---:|-----------------|
| ONE         |     |     |     |  X  |     | (0,)            |
| TWO         |     |     |  X  |     |     | (1,)            |
| THREE       |     |  X  |     |     |     | (2,)            |
| FOUR        |  X  |     |     |     |     | (3,)            |
| FIVE        |     |     |  X  |  X  |     | (0, 1)          |
| SIX         |     |  X  |  X  |     |     | (1, 2)          |
| SEVEN       |  X  |  X  |     |     |     | (2, 3)          |
| EIGHT       |     |  X  |     |  X  |     | (0, 2)          |
| NINE        |  X  |     |  X  |     |     | (1, 3)          |
| ZERO        |     |  X  |  X  |  X  |     | (0, 1, 2)       |
| UP_ARROW    |     |     |     |  X  |  X  | (0, 4)          |
| DOWN_ARROW  |     |     |  X  |     |  X  | (1, 4)          |
| RIGHT_ARROW |     |  X  |     |     |  X  | (2, 4)          |
| LEFT_ARROW  |  X  |     |     |     |  X  | (3, 4)          |
| PAGE_UP     |     |     |  X  |  X  |  X  | (0, 1, 4)       |
| PAGE_DOWN   |  X  |  X  |     |     |  X  | (2, 3, 4)       |
| END         |     |  X  |  X  |  X  |  X  | (0, 1, 2, 4)    |
| DELETE      |     |  X  |     |  X  |  X  | (0, 2, 4)       |
| INSERT      |  X  |     |  X  |     |  X  | (1, 3, 4)       |
| HOME        |  X  |  X  |  X  |     |  X  | (1, 2, 3, 4)    |

## Layer 3: Whitespace & Delimiters

| Action         | Pky | Rng | Mid | Idx | Thm | Chord         |
| -------------- | :-: | :-: | :-: | :-: | :-: | ------------- |
| ESCAPE         |     |     |     |  X  |     | (0,)          |
| TAB            |     |     |  X  |     |     | (1,)          |
| PERIOD         |     |  X  |     |     |     | (2,)          |
| MINUS          |  X  |     |     |     |     | (3,)          |
| FORWARD_SLASH  |  X  |  X  |     |     |     | (2, 3)        |
| ENTER          |     |     |  X  |  X  |     | (0, 1)        |
| COMMA          |     |  X  |     |  X  |     | (0, 2)        |
| LEFT_BRACKET   |  X  |     |  X  |     |     | (1, 3)        |
| RIGHT_BRACKET  |  X  |     |     |  X  |     | (0, 3)        |
| BACKSLASH      |  X  |  X  |  X  |     |     | (1, 2, 3)     |
| BACKSPACE      |     |  X  |  X  |     |     | (1, 2)        |
| QUOTE          |  X  |     |  X  |  X  |     | (0, 1, 3)     |
| SEMICOLON      |  X  |  X  |     |  X  |     | (0, 2, 3)     |
| GRAVE_ACCENT   |  X  |  X  |  X  |  X  |     | (0, 1, 2, 3)  |
| DELETE         |     |  X  |  X  |  X  |     | (0, 1, 2)     |

## Layer 4: Modifiers & Navigation (SCAG)

| Action         | Pky | Rng | Mid | Idx | Thm | Chord   |
| -------------- | :-: | :-: | :-: | :-: | :-: | ------- |
| LEFT_SHIFT     |  X  |     |     |     |     | (3,)    |
| LEFT_CONTROL   |     |  X  |     |     |     | (2,)    |
| LEFT_ALT       |     |     |  X  |     |     | (1,)    |
| LEFT_GUI       |     |     |     |  X  |     | (0,)    |
| RIGHT_ALT (⌥)  |     |     |  X  |  X  |     | (0, 1)  |

## Layer 5: Mouse Control (Movement, Scroll, Buttons)

| Action         | Pky | Rng | Mid | Idx | Thm | Chord        |
| -------------- | :-: | :-: | :-: | :-: | :-: | ------------ |
| MOVE UP        |     |     |     |  X  |  X  | (0, 4)       |
| MOVE DOWN      |     |     |  X  |     |  X  | (1, 4)       |
| MOVE RIGHT     |     |  X  |     |     |  X  | (2, 4)       |
| MOVE LEFT      |  X  |     |     |     |  X  | (3, 4)       |
| SCROLL UP      |     |     |  X  |  X  |  X  | (0, 1, 4)    |
| SCROLL DOWN    |  X  |  X  |     |     |  X  | (2, 3, 4)    |
| LEFT CLICK     |  X  |  X  |     |     |     | (3, 2)       |
| RIGHT CLICK    |     |     |  X  |  X  |     | (0, 1)       |
| MIDDLE CLICK   |     |     |  X  |     |     | (1, 1)       |
| FORWARD CLICK  |  X  |     |     |  X  |     | (0, 3)       |
| HOLD LEFT      |     |  X  |  X  |  X  |     | (0, 1, 2)    |
| RELEASE LEFT   |  X  |     |  X  |  X  |     | (0, 1, 3)    |
| ACCELERATE     |  X  |  X  |  X  |     |     | (1, 2, 3)    |

## Layer 6: Media

| Action               | Pky | Rng | Mid | Idx | Thm | Chord        |
| -------------------- | :-: | :-: | :-: | :-: | :-: | ------------ |
| BRIGHTNESS_DECREMENT |     |     |     |  X  |     | (0,)         |
| BRIGHTNESS_INCREMENT |     |     |  X  |     |     | (1,)         |
| VOLUME_DECREMENT     |     |  X  |     |     |     | (2,)         |
| VOLUME_INCREMENT     |  X  |     |     |     |     | (3,)         |
| MUTE                 |     |     |  X  |  X  |     | (0, 1)       |
| PLAY_PAUSE           |  X  |  X  |     |     |     | (2, 3)       |
| SCAN_NEXT_TRACK      |     |  X  |     |  X  |     | (0, 2)       |
| SCAN_PREVIOUS_TRACK  |  X  |     |  X  |     |     | (1, 3)       |
| FAST_FORWARD         |  X  |     |     |  X  |     | (0, 3)       |
| REWIND               |     |  X  |  X  |     |     | (1, 2)       |
| STOP                 |     |  X  |  X  |  X  |     | (0, 1, 2)    |
| EJECT                |  X  |     |  X  |  X  |     | (0, 1, 3)    |

## Layer 7: F1 - F12

| Action | Pky | Rng | Mid | Idx | Thm | Chord        |
| ------ | :-: | :-: | :-: | :-: | :-: | ------------ |
| F1     |     |     |     |  X  |     | (0,)         |
| F2     |     |     |  X  |     |     | (1,)         |
| F3     |     |  X  |     |     |     | (2,)         |
| F4     |  X  |     |     |     |     | (3,)         |
| F5     |     |     |  X  |  X  |     | (0, 1)       |
| F6     |     |  X  |  X  |     |     | (1, 2)       |
| F7     |  X  |  X  |     |     |     | (2, 3)       |
| F8     |     |  X  |     |  X  |     | (0, 2)       |
| F9     |  X  |     |  X  |     |     | (1, 3)       |
| F10    |     |  X  |  X  |  X  |     | (0, 1, 2)    |
| F11    |  X  |  X  |  X  |     |     | (1, 2, 3)    |
| F12    |  X  |  X  |     |  X  |     | (0, 2, 3)    |

---

## Typing Speed

Typing speed on the cinco is ~30 WPM. It is fast enough to not be frustrated. Slow enough to improve on.

That is about the same as my typing speed:

* thumb typing speed on my phone
* one handed on a qwerty full size keyboard
---

## Bill of Materials

cinco-cinco keypad

| Designators | Qty | Value               | Footprint                 |
|-------------|-----|---------------------|---------------------------|
| R1–R4       | 4   | 10 kΩ               | SMD 0805 resistor         |
| J1          | 1   | Conn_01x04_Socket   | JST-SH 4-pin connector    |
| U1          | 1   | MCP23008-xSS        | SSOP-20 package           |
| SW1–SW5     | 5   | SW_Push             | Kailh PG1350 switch socket|
| JP1         | 1   | SolderJumper_2_Open | 2-pin solder jumper       |

BLE Controller Breakout nRF52840 Nice Nano v2

| Designators | Qty | Value                    | Footprint                 |
|-------------|-----|--------------------------|---------------------------|
| U1          | 1   | Nice! Nano (ProMicro)    | ProMicro module           |
| J2          | 1   | Conn_01x04_Socket        | JST-SH 4-pin connector    |
| J1          | 1   | Conn_01x02_Socket        | JST-PH 2-pin connector    |
| SW1         | 1   | SW_SPST                  | SMD slide switch          |


