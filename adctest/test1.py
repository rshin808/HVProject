#!/user/bin/python
# This is a simple test for the adc

import smbus
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.output(11, True)
time.sleep(0.5)

bus = smbus.SMBus(1)

ADDR = 0x20
VMAX = 5

def write_addr(cmd):
    bus.write_byte(ADDR, cmd)

def write_single_byte(cmd, data):
    bus.write_i2c_block_data(ADDR, cmd, [data])

def write_two_byte(cmd, data1, data2):
    bus.write_i2c_block_data(ADDR, cmd, [data1, data2])

def startup():
    write_two_byte(0x02, 0x08, 0x88)
    write_addr(0x00)

def get_readings():
    GPIO.output(11, False)
    time.sleep(0.001)
    GPIO.output(11, True)
    time.sleep(0.001)
    return bus.read_i2c_block_data(ADDR, 0x00)

try:
    startup()
    write_addr(0x00)

    while(True):
        print get_readings()
        time.sleep(1)             

except Exception, e:
    print e
    GPIO.cleanup()
    print ""
    exit()  
