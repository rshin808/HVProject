import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(24, gpio.IN)
def my_callback(channel):
    global start
    global end
    end = time.time()
    print str(end)
try:
    gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(16, gpio.FALLING, callback = my_callback, bouncetime = 300)
    start = time.time()
    end = time.time()
    while(True):
        if ( (end - start)) > 0.5:
            start = time.time()
        if(gpio.event_detected(16)):
            print "pressed"
       
except KeyboardInterrupt:
    gpio.cleanup()
