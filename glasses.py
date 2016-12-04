from microbit import *
import neopixel
import radio
message=None
uart.init(baudrate=115200)
OFF=(0,0,0)
COLOURS=[
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
np=neopixel.NeoPixel(pin0,24)
def syncSpin(n=2,colour=(255,0,0),delay=30):
    #for x in range(n):
    while True:
        for num in range(len(np)/2):
            col=COLOURS[(17*num)%12]
            np[num] = col
            np[(num+int(len(np)/2))%len(np)] = col
            np[(num-1)%len(np)] = OFF
            np[(num+int(len(np)/2)-1)%len(np)] = OFF
            np.show()
            sleep(delay)
            message=radio.receive()
            if message:
#                uart.write("A")
                break
        if message:
#            uart.write("B")
            break
    torchOn()
def torchOn(level=255):
    for num in range(len(np)):
        np[num]=(0,0,level)
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
    elif(message == "torchOn"):
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
    else:
        uart.write(message)
