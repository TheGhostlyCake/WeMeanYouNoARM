from microbit import *
import neopixel

np = neopixel.NeoPixel(pin0, 12)
compassMode=False
compass.calibrate()
while True:
    for num in range(len(np)):
        np[num] = (255,255,255)
        np.show()
