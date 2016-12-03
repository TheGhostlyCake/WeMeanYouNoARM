from microbit import *
import neopixel
import music
import random
MUSIC_PIN = pin1
CLOCK_LEVEL = 100
uart.init(baudrate=115200,tx=None,rx=pin2)
musics=[
    music.DADADADUM,
    music.ENTERTAINER,
    music.PRELUDE,
    music.ODE,
    music.NYAN,
    music.BIRTHDAY,
    music.WEDDING,
    music.FUNERAL,
    music.WAWAWAWAA]
# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 12)
compassMode=False
leds_crazy=False
led_level=0
compass.calibrate()
while True:
    line=uart.readline()
    #line="12,4\n"
    if(line != None and line[0]==59): # 59 = ;
        # string looks like ;[a-zA-Z0-9]*
        uart.write(line)
        display.scroll(str(line)[3:-2])
    elif(line != None and line[0]==124): # 124=|
        button_b.was_pressed()
        music.play(musics[random.randrange(len(musics))],pin=MUSIC_PIN,wait=False,loop=True)
        leds_crazy=True
    elif(line != None and len(line)>1 and b',' in line and not compassMode):
      try:
        uart.write(line)
        # string looks like [0-9][0-9]?,[0-9][0-9]?,[0-9][0-9]?\n
        spl=line.split(b',')
        red=(int(spl[0])-1+5)%12
        green=(int(spl[1])-1+5)%12
        blue=(int(spl[2])-1+5)%12
        for num in range(len(np)):
            np[num] = (CLOCK_LEVEL if num==red else 0,CLOCK_LEVEL if num==green else 0,CLOCK_LEVEL if num==blue else 0)
        np.show()
        sleep(10)
      except:
        uart.write("\r\ni crash :(\r\n")
        
    if(button_a.was_pressed()):
        uart.write("\nbutton a\n")
        # enable compass mode
        if(compassMode):
            # disable compass mode
            uart.write("\r\ndisable compass\r\n")
            compassMode=False
        elif(not compassMode):
            # enable compass mode
            uart.write("\r\nenable compass\r\n")
            compassMode=True
    if(compassMode):
#            uart.write("\r\nget heading\r\n")
            heading=compass.heading()
            heading=(-round(heading/30)+4)%12
            for num in range(len(np)):
                np[num] = (20 if num==heading else 0,0,20 if num==heading else 0)
            np.show()
    if(button_b.was_pressed()):
        music.stop(MUSIC_PIN)
        leds_crazy=False
    if(leds_crazy):
        led_level=0 if led_level==255 else 255
        for num in range(len(np)):
            np[num]=(led_level,led_level,led_level)
        np.show()
