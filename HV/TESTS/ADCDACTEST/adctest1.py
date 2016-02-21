import smbus as i2c
import RPi.GPIO as GPIO
from ad7998_1 import *

GPIO.setmode(GPIO.BCM)
I2C = i2c.SMBus(1)

ADC = AD7998_1(CONVST = 17, ADDRESS = 0x21)

ADC.init_adc(GPIO) 
ADC.init_adc_bus(I2C, GPIO)

try:
    while(True):
        ADC.get_data(I2C, GPIO)
        i = 0
        for value in ADC:
            print str(i) + ":" + str(value)
            i += 1
        time.sleep(0.5)
except KeyboardInterrupt, e:
    I2C.close()
    GPIO.cleanup()


