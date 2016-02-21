import smbus
import RPi.GPIO as gpio
import time
from ad7998_1Functions import *
from ad5696Functions import *
import csv

gpio.setmode(gpio.BCM)
time.sleep(0.5)

i2c = smbus.SMBus(1)

ch = int(0b00000011)

AD5696Functions["initAD5696"](["b", "d", "1"])
AD5696Functions["outputV"](["d", "0"])
AD5696Functions["outputV"](["b", "0"])
AD7998_1Functions["initAD7998_1"]([ch])
AD7998_1Functions["readADC"]([ch])


try:
    v = 0
    v2 = 4.98
    while(True):
        if v >= 4.98:
            v = 0
        else:
            v += 0.00625
        
        if v2 <= 0:
            v2 = 4.98
        else:
            v2 -= 0.00625

        i2c = smbus.SMBus(1)
        AD5696Functions["outputV"](["d", v])
        AD5696Functions["outputV"](["b", v2])
        print AD7998_1Functions["readADC"]([ch])
        time.sleep(0.005)
except KeyboardInterrupt, e:
    i2c.close()
    gpio.cleanup()
