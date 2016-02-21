import RPi.GPIO as gpio
from encoder2b_int import *

gpio.setmode(gpio.BCM)

print PINS

ENC = Encoder2b(PINS)
ENC.initEncoder(gpio)

try:

    while(True):
        check = ENC.waitHold(gpio)
        direction = ENC.getDirection(gpio)

        if check != None:
            print check
        if direction != None:
            print direction
except KeyboardInterrupt, e:
    gpio.cleanup()
    exit()

