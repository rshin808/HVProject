#!/usr/bin/env python
# This simply sets all the output high

import smbus
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, True)
time.sleep(0.5)

bus = smbus.SMBus(1)

ADDR = 0x0C
CMD = 0x1F
DATA = [0xFF, 0xFF]
bus.write_i2c_block_data(ADDR, CMD, DATA)

try:
    while(True):
        pass
except KeyboardInterrupt:
    GPIO.output(7,False)
    time.sleep(0.5)
    GPIO.cleanup()

