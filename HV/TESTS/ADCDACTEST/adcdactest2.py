import smbus
import RPi.GPIO as gpio
import time
from ad7998_1 import *
from ad5696Functions import *

gpio.setmode(gpio.BCM)
time.sleep(0.5)

i2c = smbus.SMBus(1)

ADC = AD7998_1(CONVST = 17, ADDRESS = 0x21)

ADC.init_adc(gpio)
ADC.init_adc_bus(i2c, gpio)

AD5696Functions["initAD5696"](["d", "1"])
AD5696Functions["outputV"](["d", "0"])

try:
    v = 0
    while(True):
        if v >= 4.95:
            v = 0
        else:
            v += 0.02

        AD5696Functions["outputV"](["d", v])
        """
        time.sleep(0.2)
        ADC.get_data(i2c, gpio)
        i = 0
        for value in ADC:
            if i == 0:
                print str(i) + ": " + str(value)
            i += 1
        """
except KeyboardInterrupt, e:
    i2c.close()
    gpio.cleanup()
