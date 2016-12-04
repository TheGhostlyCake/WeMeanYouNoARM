from microbit import *
import neopixel
import radio

uart.init(baudrate=115200)
OFF=(0,0,0)
np=neopixel.NeoPixel(pin0,24)
def syncSpin(n=2,colour=(255,0,0),delay=80):
    for x in range(n):
        for num in range(len(np)/2):
            np[num] = colour
            np[(num+int(len(np)/2))%len(np)] = colour
            np[(num-1)%len(np)] = OFF
            np[(num+int(len(np)/2)-1)%len(np)] = OFF
            np.show()
            sleep(delay)
def torchOn(level=255):
    for num in range(len(np)):
        np[num]=(0,0,level)
    np.show()
def torchOff():
    for num in range(len(np)):
        np[num]=OFF
    np.show()
radio.config(channel=89)
radio.on()
while True:
    message=radio.receive()
    if(not message):
        pass
    elif(message == "torchOn"):
        uart.write("on\r\n")
        torchOn()
    elif(message == "torchOff"):
        uart.write("off\r\n")
        torchOff()
    elif(message == "spin"):
        uart.write("spin\r\n")
        syncSpin()
    else:
        uart.write(message)
