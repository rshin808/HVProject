import smbus
import time
import RPi.GPIO as gpio
import sys
from AD7998_1REGS import *

i2c = smbus.SMBus(1)
gpio.setmode(gpio.BCM)

class ADCDefaults:
    CONVST = 17
    VREF = 5
    RES = 12
    VMAX = 5
    VLOW = 0
    ADDRESS = 0x21

gpio.setup(ADCDefaults.CONVST, gpio.OUT)

def initAD7998_1(params):
    global gpio
    global i2c
    gpio.setup(ADCDefaults.CONVST, gpio.OUT)
    gpio.output(ADCDefaults.CONVST, False)
    gpio.output(ADCDefaults.CONVST, True)
    time.sleep(0.000001)
    gpio.output(ADCDefaults.CONVST, False)
    time.sleep(0.000002)
    enabled = int(params[0])
    dataH = 0x00
    dataH |= ((enabled >> 4) & 0x0f)
    dataL = 0x00
    dataL |= (enabled & 0x0f) << 4
    dataL |= 0x0b
    i2c.write_byte(ADCDefaults.ADDRESS, 0x00)
    i2c.write_i2c_block_data(ADCDefaults.ADDRESS, 0x02, [dataH, dataL])

def readADC(params):
    global gpio
    global i2c
    channels = int(params[0])
    conversion = []
    for i in range(8):
        if (channels & 2 ** i) == 2 ** i:
            gpio.output(ADCDefaults.CONVST, True)
            time.sleep(0.000001)
            gpio.output(ADCDefaults.CONVST, False)
            time.sleep(0.000002)
            data = i2c.read_i2c_block_data(ADCDefaults.ADDRESS, 0x00)
            valueH = 0x0f & data[0]
            valueL = 0xff & data[1]
            value = (valueH << 8) | valueL
            conversion.append(value)
    return conversion

def close():
    global gpio
    global i2c
    i2c.close()
    gpio.cleanup()

AD7998_1Functions = {
    "initAD7998_1"  :   initAD7998_1,
    "readADC"       :   readADC,
    "close"         :   close,
} 

#func = sys.argv[1]
#params = list(sys.argv[2:])
#AD7998_1Functions[func](params)
