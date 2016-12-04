#    This file is part of SmartWatch.
#
#    SmartWatch is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    SmartWatch is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with SmartWatch.  If not, see <http://www.gnu.org/licenses/>.

from microbit import *
import neopixel
import radio
message=None # preset the 
uart.init(baudrate=115200) # purely for debugging
OFF=(0,0,0) # easier than typing the triple each time...
COLOURS=[ # Copy of the colours from 'yay watch.py' for use in party mode
(0x89,0x00,0x00),
(0x58,0x3D,0x00),
(0x37,0x89,0x00),
(0x00,0x88,0x14),
(0x00,0x47,0x4A),
(0x00,0x38,0x80),
(0x00,0x00,0x95),
(0x17,0x00,0x86),
(0x39,0x00,0x65),
(0x48,0x00,0x37),
(0x7D,0x00,0x17),
(0x85,0x00,0x08)]
np=neopixel.NeoPixel(pin0,24) # Initialise the neopixel rings (2*12=24)
def syncSpin(n=2,colour=(255,0,0),delay=30): # Party mode
    while True: # Display all of the fun colours
        for num in range(len(np)/2):
            col=COLOURS[(17*num)%12]
            np[num] = col # All duplicated across both rings
            np[(num+int(len(np)/2))%len(np)] = col
            np[(num-1)%len(np)] = OFF
            np[(num+int(len(np)/2)-1)%len(np)] = OFF
            np.show()
            sleep(delay)
            message=radio.receive() # Keep checking for incoming messages
            if message:
#                uart.write("A")
                break
        if message:
#            uart.write("B")
            break
    red() # A bit of a hack. This is the next part in the cycle
def torchOn(level=255): # Blue
    for num in range(len(np)):
        np[num]=(0,0,level)
    np.show()
def red(level=255):
    for num in range(len(np)):
        np[num]=(level,0,0)
    np.show()
def green(level=255):
    for num in range(len(np)):
        np[num]=(0,level,0)
    np.show()
#    message=radio.receive()
def torchOff():
    for num in range(len(np)):
        np[num]=OFF
    np.show()
#    message=radio.receive()
radio.config(channel=89)
radio.on()
while True:
    if not message:
#        uart.write("C")
        message=radio.receive()
    if(not message):
        pass
    elif(message == "torchOn" or message == "blue"):
#        display.scroll("1")
        message=None
        torchOn()
    elif(message == "torchOff"):
#        display.scroll("0")
        message=None
        torchOff()
    elif(message == "spin"):
#        display.scroll("8")
        message=None
        syncSpin()
    elif(message == "red"):
        red()
        message=None
    elif(message == "green"):
        green()
        message=None
    else:
        uart.write(message)
