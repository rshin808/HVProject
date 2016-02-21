import smbus
import RPi.GPIO as gpio
import time
from ad7998_1Functions import *
from ad5696Functions import *
import csv

gpio.setmode(gpio.BCM)
time.sleep(0.5)

i2c = smbus.SMBus(1)

ch = int(0b00000101)

AD5696Functions["initAD5696"](["d", "1"])
AD5696Functions["outputV"](["d", "0"])
AD7998_1Functions["initAD7998_1"]([ch])
AD7998_1Functions["readADC"]([ch])


try:
    v = 0
    while(True):
        if v >= 4.95:
            v = 0
        else:
            v += 0.00625
        i2c = smbus.SMBus(1)
        AD5696Functions["outputV"](["d", v])
        print AD7998_1Functions["readADC"]([ch])
        time.sleep(0.02)
except KeyboardInterrupt, e:
    i2c.close()
    gpio.cleanup()
