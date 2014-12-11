#! /usr/bin/python

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

#spi.max_speed_hz = 120000000
spi.mode = 3

def reg(index, value):
    # Index and value are integers
    # Send Index
    gpio.output(RS, False)
    spi.xfer2([index])
    gpio.output(RS, True)

    # Send Value
    spi.xfer2([value])

def data_start():
    gpio.output(RS, False)
    spi.xfer2([0x22])
    gpio.output(RS, True)

def data(value):
    v1 = "{0:b}".format(value)[:-8].zfill(8)
    v2 = "{0:b}".format(value)[-8:]
    spi.xfer2([int(v1, 2), int(v2, 2)])

def set_region(x1, y1, x2, y2):
    # Define the boundaries
    reg(0x17, x1)
    reg(0x18, x1 + x2 - 1)
    reg(0x19, y1)
    reg(0x1A, y1 + y2 - 1)

    # Initialize start parameters
    reg(0x20, x1)
    reg(0x21, y1)

reg(0x04, 0x03)
time.sleep(0.002)
reg(0x04, 0x00)
time.sleep(0.002)

reg(0x3B, 0x01)

reg(0x03, 0x90)

reg(0x80, 0x01)

reg(0x08, 0x04)
reg(0x09, 0x05)
reg(0x0A, 0x05)

reg(0x0B, 0x9D)
reg(0x0C, 0x8C)
reg(0x0D, 0x57)

reg(0x10, 0x56)
reg(0x11, 0x4D)
reg(0x12, 0x46)

reg(0x13, 0xA0)

reg(0x29, 0x00)

reg(0x14, 0x01)
reg(0x16, 0x66)

reg(0x06, 0x01)

set_region(0, 0, 160, 128)

data_start()

for pixel in range(160 * 128):
    data(0xFFFF)

print "waiting"
try:
     while(True): 
         pass
except KeyboardInterrupt:
     reg(0x06, 0x00)
     gpio.output(RES, True)
     gpio.cleanup()
     print ""
