#! /usr/bin/python

check = 0xDFFF

import spidev
import time
import RPi.GPIO as gpio

RES = 8
RS = 12
gpio.setmode(gpio.BOARD)
gpio.setup(RES, gpio.OUT)
gpio.output(RES, True)
gpio.setup(RS, gpio.OUT)
gpio.output(RS, False)
time.sleep(1)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000000
spi.mode = 3

def seps525_reg(address, value):
    # CS low
    # RS low
    # send address
    # RS high
    # CS high
    # CS low
    # send value
    # CS high
    gpio.output(RS, False)
    spi.xfer2([address])
    gpio.output(RS, True)
    spi.xfer2([value])

def data(value):
    v1 = int("{0:b}".format(value)[:-8].zfill(8), 2)
    v2 = int("{0:b}".format(value)[-8:], 2)
    gpio.output(RS, True)
    spi.xfer2([v1, v2])
    gpio.output(RS, False)

def seps525_init():
    # startup RS
    gpio.output(RS, False)
    time.sleep(0.5)
    gpio.output(RS, True)
    time.sleep(0.5)

    # set normal driving current
    # disable oscillator power down
    seps525_reg(0x04, 0x01)
    time.sleep(0.002)

    # enable power save mode
    # set normal driving current
    # disable oscillator power down
    seps525_reg(0x04, 0x00)
    time.sleep(0.002)

    seps525_reg(0x3B, 0x00)

    # set EXPORT1 at internal clock
    seps525_reg(0x02, 0x01)

    # set framerate as 120 Hz
    seps525_reg(0x03, 0x90)

    # set reference voltage controlled by external resistor
    seps525_reg(0x80, 0x01)

    # set pre-charge time
    # red
    seps525_reg(0x08, 0x04)
    # green
    seps525_reg(0x09, 0x05)
    # blue  
    seps525_reg(0x0A, 0x05)

    # set pre-charge current
    # red
    seps525_reg(0x0B, 0x9D)
    # green
    seps525_reg(0x0C, 0x8C)
    # blue
    seps525_reg(0x0D, 0x57)

    # set driving current
    # red
    seps525_reg(0x10, 0x56)
    # green
    seps525_reg(0x11, 0x4D)
    # blue 
    seps525_reg(0x12, 0x46)

    # set color sequence
    seps525_reg(0x13, 0x00)
        
    # set MCU interface mode
    seps525_reg(0x14, 0x11)
    seps525_reg(0x16, 0x66)
    
    # shift mapping RAM counter
    seps525_reg(0x20, 0x00)
    seps525_reg(0x21, 0x00)

    # 1/128 duty
    seps525_reg(0x28, 0x7F)

    # set mapping
    seps525_reg(0x29, 0x00)

    # display on
    seps525_reg(0x06, 0x01)

    # disable power savvve mode
    seps525_reg(0x05, 0x00)

    # set RGB polarity
    seps525_reg(0x15, 0x00)

def init_oled_display():
    seps525_reg(0x17, 0x00)
    seps525_reg(0x18, 0x09F)
    seps525_reg(0x19, 0x00)
    seps525_reg(0x1A, 0x7F)
    data_start()
    time.sleep(1)

def data_start():
    gpio.output(RS, False)
    spi.xfer2([0x22])
    gpio.output(RS, True)

def seps525_set_region(width1, height1, width2, height2):
    seps525_reg(0x17, width1)
    seps525_reg(0x18, width1 + width2 - 1)
    seps525_reg(0x19, height1)
    seps525_reg(0x1A, height1 + height2 - 1)
    seps525_reg(0x20, width1)
    seps525_reg(0x21, height1)

seps525_init()
seps525_set_region(0, 0, 160, 128)
data_start()
print "drawing"
for pixel in range((160 * 128)):
    data(check)
print "done1"
    

try:
    while(True):
        pass
except KeyboardInterrupt:
    seps525_reg(0x06, 0x00)
    gpio.output(RES, True)
    gpio.cleanup()
    exit()    
