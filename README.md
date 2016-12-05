### laurie is a fool.
### so is tom

![tom](https://scontent-lhr3-1.xx.fbcdn.net/v/t1.0-1/p160x160/12790933_1156615257682396_3499364541870816633_n.jpg?oh=21bb12d8ddce3594d4780a9cacab74f0&oe=58C25E22)

# Bluetooth-synchronised Micro:bit smartwatch
## ~~ An inspiring vision of the future ~~
Authors: *David Young, Laurie Kirkcaldy, Josh Curry, Tom Charter*

For the December 2016 ARM Hackathon, we decided to make a smart watch.

## Specification
* Display the time on an analogue display with a ring of 12 `WS2812` LEDs
* Synchronise the time to a BLE server
* Engage and disengage *compass mode* by pressing the buttons
* Set an alarm via a web interface, and cancel a ringing alarm by shaking. Alarm mode can be identified by some awesome tunes and strobing LEDs

## Overview
### Watch
Two microbits are used in the main body of the watch. One (programmed with embedded C) handles the bluetooth low energy communication, timing and alarm

## Bluetooth Characteristics
* Time
    * Laurie wants:
    * HHMMSS as 3 hex bytes (raw data would be nice, not ascii)
    * 24 hour time (dunno how we show AM/PM, they should just look out the window)
