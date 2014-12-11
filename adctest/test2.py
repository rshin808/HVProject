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

ADDR = 0x23
VMAX = 5
RES = 12

def get_channel(binary_string):
    return int(binary_string[-3:], 2) + 1

def int_to_binary8(input_int):
    return "{0:b}".format(input_int).zfill(8)

def convert_int_to_voltage(input_int):
    return ((float(input_int) / float(2 ** RES)) * float(VMAX))
    

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
        data = get_readings()[:2]
        data1 = int_to_binary8(data[0])
        data2 = int_to_binary8(data[1])
        print "CH" + str(get_channel(data1[:4])) + ": "
        voltage_binary = data1[4:] + data2
        print convert_int_to_voltage(int(voltage_binary, 2))
        time.sleep(1)             

except Exception, e:
    print e
    GPIO.cleanup()
    print ""
    exit()  
