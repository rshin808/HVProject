import RPi.GPIO as GPIO
import smbus as i2c
from ad5696 import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, False)
time.sleep(.5)
I2C = i2c.SMBus(1)

DAC = AD5696(RESET = 15)
DAC.init_dac_address(GPIO)
DAC.update_voltages([1, 1, 1, 1])
DAC.output_voltages(I2C)
print str(DAC._voltages)

try:
    while(1):
        pass
except KeyboardInterrupt, e:
    GPIO.cleanup()
    I2C.close()
