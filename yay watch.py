from microbit import *
import neopixel
import music
import random
import radio
MUSIC_PIN = pin1 # buzzer is connected here
CLOCK_LEVEL = 100 # LED level for the clock display
NOTIFICATION_COLOUR=[ # Rainbow colours
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

uart.init(baudrate=115200,tx=None,rx=pin2) # set up serial. Rx from other microbit, Tx to usb serial for debug
musics=[ # selection of pretty tunes for the alarm mode
    music.DADADADUM,
    music.ENTERTAINER,
    music.PRELUDE,
    music.ODE,
    music.NYAN,
    music.BIRTHDAY,
    music.WEDDING,
    music.WAWAWAWAA]
# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin0, 12) # 12 neopixels connected to pin 0
compassMode=False # set some flags for later
leds_crazy=False
led_level=0
#compass.calibrate()
radioFunctions=["red","green","blue","torchOff","spin"] # functions supported by the glasses
radio_current=0 # state variable for the glasses
def fun(i):
 "Displays a fun swirling pattern that loops i times"
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
music.play(music.POWER_UP,pin=MUSIC_PIN,wait=False,loop=False) # Startup tune
fun(2) # ...and some pretty lights
radio.config(channel=89) # set the radio channel away from the default
radio.on() # self-explanatory
while True: # main loop
    buttonA=button_a.was_pressed()
    line=None
    if(uart.any()): # Check for a line in the serial buffer
        line=uart.readline()
    #line="12,4\n"
    if(line != None and line[0]==59): # 59 = ;
        # string looks like ;[a-zA-Z0-9]*
      if(b"FB!" in line): # Magic code to trigger facebook notification light and sound
          for num in range(len(np)):
              np[num]=(0,0,100) # blue
          np.show()
          music.play(music.BA_DING,pin=MUSIC_PIN,wait=True,loop=False)
      elif(b"SLACK" in line): # Code for slack notification light and sound
          for num in range(len(np)):
              np[num]=(0,128,100) # teal
          np.show()
          music.play(music.BA_DING,pin=MUSIC_PIN,wait=True,loop=False)
      else: # some other text notification
        music.play(music.POWER_UP,pin=MUSIC_PIN,wait=False,loop=False) # This tune will not get annoying
        for num in range(len(np)): # turn off the LEDs so that the swirly colours work
            np[num]=(0,0,0)
        np.show()
        for num in range(len(np)): # Display the swirly rainbow
            np[num]=NOTIFICATION_COLOUR[num]
            np.show()
            sleep(80)
        uart.write(line) # print the received string for debug
        display.scroll(str(line)[3:-3],wait=False,monospace=True) # Horrible bodge to strip 'b"hi"\n' down to 'hi'
        fun(round(.78*len(str(line)[3:-3]))) # Swirly pattern for the duration of the message
    elif(line != None and line[0]==124): # 124=| # Magic code for triggering the alarm sound and flashing lights
        button_b.was_pressed() # Reset the counter on button_b so that we can use it to reset the alarm
        music.play(musics[random.randrange(len(musics))],pin=MUSIC_PIN,wait=False,loop=True) # yay song
        leds_crazy=True # set the flag for later
    elif(line != None and len(line)>1 and b',' in line and not compassMode):
      # This part decodes the time display signals
      try: # Totally not a bodge in case of malformed packets...
        uart.write(line) # debug message
        # string looks like [0-9][0-9]?,[0-9][0-9]?,[0-9][0-9]?\n
        spl=line.split(b',') # choppu!
        red=(int(spl[0])-1+5)%12 # takes a 1-indexed position and aligns it to the display
        green=(int(spl[1])-1+5)%12
        blue=(int(spl[2])-1+5)%12
        for num in range(len(np)): # display them
            np[num] = (CLOCK_LEVEL if num==red else 0,CLOCK_LEVEL if num==green else 0,CLOCK_LEVEL if num==blue else 0)
        np.show()
        sleep(10) # This made it not break early on. Code has not been tested without this line.
      except:
        # In the event of a malformed packet or any other error, quietly complain to the debug console
        uart.write("\r\ni crash :(\r\n")
        
    if(buttonA):
        uart.write("\nbutton a\n")
        # enable compass mode
        if(compassMode):
            # disable compass mode
            # sets the flag and the next branch statement deals with the compass details
            uart.write("\r\ndisable compass\r\n")
            compassMode=False
            sleep(10)
        elif(not compassMode):
            # enable compass mode
            # same as above, but the other way round
            uart.write("\r\nenable compass\r\n")
            compassMode=True
            sleep(10)
    if(compassMode):
#            uart.write("\r\nget heading\r\n")
            heading=compass.heading() # get the heading.
            # If compass.calibrate() has not been called then it is run automatically
            heading=(-round(heading/30)+4)%12 # Scale and align
            for num in range(len(np)): # Display compass heading on the neopixel ring
                np[num] = (20 if num==heading else 0,0,20 if num==heading else 0)
            np.show()
    if(button_b.was_pressed() or (line is not None and line[0] == 42)): # 42 = *
        # button_b cancels the alarm and pages through modes on the smart glasses
        uart.write("\r\nButton b was pressed\r\n")
        if(leds_crazy): # cancel alarm if it is running
            music.stop(MUSIC_PIN)
            leds_crazy=False
        radio_current=(radio_current+1)%len(radioFunctions) # Increment the glasses state variable
        uart.write("\r\nradio %i\r\n"%radio_current) # debug
        radio.send(radioFunctions[radio_current]) # Send the desired command to all listening smart glasses
    if(leds_crazy): # do some strobe
        led_level=0 if led_level==255 else 255 # Toggle the brightness between 0 and 255
        for num in range(len(np)): # And then turn all LEDs on or off as appropriate.
            np[num]=(led_level,led_level,led_level)
        np.show()
