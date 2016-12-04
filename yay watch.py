from microbit import *
import neopixel
import music
import random
import radio
MUSIC_PIN = pin1
CLOCK_LEVEL = 100
NOTIFICATION_COLOUR=[
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

uart.init(baudrate=115200,tx=None,rx=pin2)
musics=[
    music.DADADADUM,
    music.ENTERTAINER,
    music.PRELUDE,
    music.ODE,
    music.NYAN,
    music.BIRTHDAY,
    music.WEDDING,
    music.WAWAWAWAA]
# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 12)
compassMode=False
leds_crazy=False
led_level=0
#compass.calibrate()
radioFunctions=["torchOn","torchOff","spin"]
radio_current=0
def fun(i):
 for num in range(len(np)):
    np[num]=NOTIFICATION_COLOUR[num]
    np.show()
    sleep(80)
 for nom in range(i*12):
  for num in range(len(np)):
      np[(num+nom)%12] = NOTIFICATION_COLOUR[num]
  np.show()
  sleep(80)
 for num in range(len(np)):
    np[num]=(0,0,0)
    np.show()
    sleep(80)
#fun(14)

music.play(music.POWER_UP,pin=MUSIC_PIN,wait=False,loop=False)
fun(2)
radio.config(channel=89)
radio.on()
while True:
    buttonA=button_a.was_pressed()
    line=None
    if(uart.any()):
        line=uart.readline()
    #line="12,4\n"
    if(line != None and line[0]==59): # 59 = ;
        # string looks like ;[a-zA-Z0-9]*
        music.play(music.POWER_UP,pin=MUSIC_PIN,wait=False,loop=False)
        for num in range(len(np)):
            np[num]=(0,0,0)
        np.show()
        for num in range(len(np)):
            np[num]=NOTIFICATION_COLOUR[num]
            np.show()
            sleep(80)
        uart.write(line)
        display.scroll(str(line)[3:-3],wait=False,monospace=True)
        fun(round(.78*len(str(line)[3:-3])))
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
        
    if(buttonA):
        uart.write("\nbutton a\n")
        # enable compass mode
        if(compassMode):
            # disable compass mode
            uart.write("\r\ndisable compass\r\n")
            compassMode=False
            sleep(10)
        elif(not compassMode):
            # enable compass mode
            uart.write("\r\nenable compass\r\n")
            compassMode=True
            sleep(10)
    if(compassMode):
#            uart.write("\r\nget heading\r\n")
            heading=compass.heading()
            heading=(-round(heading/30)+4)%12
            for num in range(len(np)):
                np[num] = (20 if num==heading else 0,0,20 if num==heading else 0)
            np.show()
    if(button_b.was_pressed() or line[0] == 166): # 166 = ¦
        uart.write("oifeshlkmd")
        if(leds_crazy):
            music.stop(MUSIC_PIN)
            leds_crazy=False
        radio_current=(radio_current+1)%len(radioFunctions)
        uart.write("\r\nradio %i\r\n"%radio_current)
        radio.send(radioFunctions[radio_current])
    if(leds_crazy):
        led_level=0 if led_level==255 else 255
        for num in range(len(np)):
            np[num]=(led_level,led_level,led_level)
        np.show()
