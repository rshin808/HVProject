import smbus
import time
import RPi.GPIO as gpio
import sys

# I2C
i2c = smbus.SMBus(1)

# GPIO
gpio.setmode(gpio.BCM)


# Defaults
class DACDefaults:
    RES = 16
    VREF = 5
    RESET = 15
    LDAC = 14
    ADDRESS = 0x0c


voltages = [0, 0, 0, 0]
enabled = 0x0

def initAD5696(params):
    global gpio
    global i2c
    global enabled
    gpio.setup(DACDefaults.RESET, gpio.OUT)
    gpio.setup(DACDefaults.LDAC, gpio.OUT)
    gpio.output(DACDefaults.RESET, False)
    time.sleep(0.1)
    gpio.output(DACDefaults.RESET, True)
    time.sleep(0.05)
    gpio.output(DACDefaults.LDAC, True)
    time.sleep(0.05)
    cmd = 0x40
    dataH = 0x00
    dataL = 0x00
    pd = int(params[-1])

    if "a" in params:
        enabled |= 0x1
    else:
        dataL |= pd
    if "b" in params:
        enabled |= 0x2
    else:
        dataL |= (pd << 2)

    if "c" in params:
        enabled |= 0x4
    else:
        dataL |= (pd << 4)

    if "d" in params:
        enabled |= 0x8
    else:
        dataL |= (pd << 6)
    
    i2c.write_i2c_block_data(DACDefaults.ADDRESS, cmd, [dataH, dataL])
    #i2c.write_byte(ADDRESS, 0x5f)  
    #i2c.write_byte(ADDRESS, 0x00)  

def v2b(voltage):
    b = (float(voltage) / 5.0 * 65535)
    if b < 0:
        b = 0
    elif b > 65535:
        b = 65535
    dataH = 0xff & (int(b) >> 8)
    dataL = 0xff & int(b)
    return [dataH, dataL]

def outputV(params):
    global enabled
    global i2c
    global gpio

    if params[0] == "a":
        data = v2b(float(params[1])) 
        #i2c.write_i2c_block_data(ADDRESS, 0x11, data) 
        #time.sleep(0.001)            
        #i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x31, data) 
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x11, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, False)
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x21, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, True)
 
    if params[0] == "b":
        data = v2b(float(params[1])) 
        #i2c.write_i2c_block_data(ADDRESS, 0x12, data) 
        #time.sleep(0.001)            
        #i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x32, data) 
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x12, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, False)
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x22, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, True)

    if params[0] == "c":
        data = v2b(float(params[1])) 
        #i2c.write_i2c_block_data(ADDRESS, 0x14, data) 
        #time.sleep(0.001)            
        #i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x34, data) 
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x14, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, False)
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x24, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, True)

    if params[0] == "d":
        data = v2b(float(params[1])) 
        #i2c.write_i2c_block_data(ADDRESS, 0x18, data) 
        #time.sleep(0.001)           
        #i2c.write_i2c_block_data(ADDRESS, 0x38, data) 
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x18, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, False)
        i2c.write_i2c_block_data(DACDefaults.ADDRESS, 0x28, data)
        time.sleep(0.01)
        gpio.output(DACDefaults.LDAC, True)
        

def close():
    global gpio
    global i2c
    i2c.close()
    gpio.cleanup()

AD5696Functions = {
    "initAD5696"    : initAD5696,
    "outputV"       : outputV,
    "close"         : close,
}

#func = sys.argv[1]
#params = list(sys.argv[2:])
#AD5696Functions[func](params)
