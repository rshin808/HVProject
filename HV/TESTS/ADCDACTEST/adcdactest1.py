import smbus as i2c
import RPi.GPIO as GPIO
import time
from ad7998_1 import *
from ad5696 import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, False)
time.sleep(0.5)

I2C = i2c.SMBus(1)

ADC = AD7998_1(CONVST = 17, ADDRESS = 0x21)

ADC.init_adc(GPIO)
ADC.init_adc_bus(I2C, GPIO)

DAC = AD5696(RESET = 15)
DAC.init_dac_address(GPIO)
DAC.update_voltages([0, 1, 1, 1])
DAC.output_voltages(I2C)
DAC.configure_enabled(channels_enabled = [0, 0, 0, 1], i2c = I2C)

try:
    v = 0
    while(True):
        if v >= 4.95:
            v = 0
        else:
            v += 0.02
        DAC.update_voltages([v, 1, 2, 3])
        GPIO.output(14, True)
        DAC.output_voltages(I2C)
        GPIO.output(14, False)
        ADC.get_data(I2C, GPIO)
        i = 0
        for value in ADC:
            if i == 0:
                print str(i) + ": " + str(value)
            i += 1
        time.sleep(0.04)
except KeyboardInterrupt, e:
    I2C.close()
    GPIO.cleanup()
