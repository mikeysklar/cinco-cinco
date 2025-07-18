# Cinco-Cinco  
*A 5-Key Wireless Chording Keyboard*

Cinco-Cinco is a low-profile chording keyboard that uses just **five
keys** to emulate a full keyboard by combining keypresses into
chords and utilizing **seven layers**.

I’ve spent the last year building pocket keyboards. My
[BUBBY](https://github.com/mikeysklar/bubby) is a daily carry which
I use for todo lists. It made me enjoy typing with one hand to the
point that I wanted a desktop version, which is what you see here.

![Screenshot](pics/cc-main.jpeg)

## Table of Contents

- [Introduction](#introduction)
- [Hardware Highlights](#hardware-highlights)
  - [Case Design](#case-design)
  - [Mechanical Switch Choice](#mechanical-switch-choice)
  - [Chording Software](#chording-software)
- [CircuitPython Compatibility](#circuitpython-compatibility)
- [Design Files & Software Versions](#design-files--software-versions)
- [Typing Speed](#typing-speed)
- [Layer Maps](#layer-maps)
  - [Layer 1: Letters](#layer-1-letters)
  - [Layer 2: Numbers](#layer-2-numbers)
  - [Layer 3: Whitespace & Delimiters](#layer-3-whitespace--delimiters)
  - [Layer 4: Modifiers & Navigation](#layer-4-modifiers--navigation)
  - [Layer 5: Mouse Control / Media](#layer-5-mouse-control--media)
  - [Layer 6: Media](#layer-6-media)
  - [Layer 7: F1 - F12](#layer-7-F1---F12)
- [BOM](#bill-of-materials)

---

## Introduction

Computing is rapidly changing. We are moving away from sitting at
desks and staring at screens. Smart glasses and watches let us
consume information on the go. Phones, which have taken too much
of our attention, no longer need to be our primary method of
communication.

**The keys are key**

Chording opens up a future of input that is compact, discreet, and
mobile. This same keyboard can also enhance desktop productivity,
allowing CAD users and creatives to use one hand for keyboard
shortcuts while the other handles precise mouse movements.

Cinco-Cinco uses just **five keys**, but can generate over 107
different key combos, including mouse actions. The thumb button
switches between **seven layers**—alphabets, numbers, punctuation,
and more. The layout is based on a modified SAIE layout, optimized so 
the most common letters require minimal finger effort.

At first, I wasn’t sure cramming so much into the thumb key would
work well. But with careful timing and logic in the firmware, it
switches layers smoothly without getting in the way.

---

![Screenshot](pics/cc-parts.jpeg)


## Hardware Highlights

- **I2C STEMMA QT connector** for plug-and-play support for different controllers  
- **Two PCB system**: one controller board and one keypad connected via STEMMA QT cable  
- **Hardware-based key detection**: MCP23008 GPIO expander running at 400 kHz for fast, accurate chord detection  
- **BLE-compatible microcontrollers**: Tested with nRF52840  
- **1200mAh battery** integrated into the case to hold keypad in place and reduce charging frequency  

![Screenshot](pics/cc-freecad.gif)

### Case Design

The case is built as a three-layer sandwich. The base has cutouts
to keep components low profile and includes heat-set inserts to
secure the mid and top layers. The PCBs have matching holes for
alignment and locking, ensuring a secure fit.

Flat, countersunk screws keep the top flush. The “Human Machine”
inlay was added late to break up the large pink area and has become
a distinctive feature.

### Mechanical Switch Choice

I chose Kailh PG1350 CHOC switches for their availability and easy
installation. Their low-profile design lets all components fit on
the PCB’s bottom side, simplifying SMT assembly. I’ve tried pink,
red, and robin egg blue switches—the blue ones feel best to type
on, despite needing more force, and they look nice too.

### Chording Software

The firmware works hard to register chords accurately despite early
challenges with false triggers and duplicates. It waits for the
first key release before registering a chord, allowing for sloppy
or staggered key presses without mistakes. It doesn’t wait for all
keys to be released — once a key lifts, the chord buffer clears,
letting you move on quickly.

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

![Screenshot](pics/cc-monkey.png)

## Typing Speed

Typing speed on the cinco is ~25 WPM. It is fast enough to not be frustrated. Slow enough to improve on.

That is about the same as my typing speed:

* thumb typing speed on my phone
* one handed on a qwerty full size keyboard


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
| U1          | 1   | Nice!Nano v2             | SuperMini nRF52840        |
| J2          | 1   | Conn_01x04_Socket        | JST-SH 4-pin connector    |
| J1          | 1   | Conn_01x02_Socket        | JST-PH 2-pin connector    |
| SW1         | 1   | SW_SPST                  | SMD slide switch          |


