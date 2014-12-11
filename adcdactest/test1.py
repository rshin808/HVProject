#!/usr/bin/python

import smbus
import time
import RPi.GPIO as gpio

#7,4 !RESET
#11,17 A1 = 0
#13,27 A0 = 0
#15,22 !LDAC = 0
#8,14 !RES
#10,15 !CS
#12,18 D/C
#16,23 ALERT/BUSY
#18,24 !CONVST
#22,24 AS

PINS = {
    "!RESET" : 7,
    "A1" : 11,
    "A0" : 13,
    "!LDAC" : 15,
    "!RES" : 8,
    "!CS" : 10,
    "D/C" : 12,
    "ALERT/BUSY" : 16,
    "!CONVST" : 18,
    "AS" : 22,
}

gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(8, gpio.OUT)
gpio.setup(10, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.IN)
gpio.setup(18, gpio.OUT)
gpio.setup(22, gpio.OUT)

gpio.output(7, True)
gpio.output(11, False)
gpio.output(13, False)
gpio.output(15, False)
gpio.output(8, True)
gpio.output(10, True)
gpio.output(12, False)
gpio.output(18, True)
gpio.output(22, False)

time.sleep(1)

RES = 12
VMAX = 5
VREF = 5

bus = smbus.SMBus(1)

ADDRADC = 0x23
ADDRDAC = 0x0C

# ADC functions
def get_channel(bin_string):
    return int(bin_string[-3:], 2) + 1

def int_to_bin8(in_int):
    return "{0:b}".format(in_int).zfill(8)

def int_to_volt(in_int):
    return ((float(in_int) / float(2 ** RES)) * float(VMAX))

def write_addr(cmd):
    bus.write_byte(ADDRADC, cmd)

def write_single_byte(cmd, data):
    bus.write_i2c_block_data(ADDRADC, cmd, [data])

def write_two_byte(cmd, data1, data2):
    bus.write_i2c_block_data(ADDRADC, cmd, [data1, data2])

def startup(cmd1, cmd2):
    write_two_byte(0x02, cmd1, cmd2)
    write_addr(0x00)  

def get_readings():
    gpio.output(18, False)
    time.sleep(0.001)
    gpio.output(18, True)
    time.sleep(0.001)
    return bus.read_i2c_block_data(ADDRADC, 0x00)

# DAC functions
def volt_to_int(volt):
    conversion = 2 ** RES - 1
    scalar = float(conversion) / float(VREF)
    return int(volt * scalar)

quit = ""
voltage = []
channels_EN = 0
lowest = 9

try:
    ch_EN1 = "0000"
    ch_EN2 = "1000"
    while(True):
        try:
            quit = input("ENABLE voltage channels 8->1 with 1's.\n>> ")
            if(str(quit).lower() == "q"):
                gpio.output(7, False)
                gpio.cleanup()
                exit() 
            if(len(str(quit)) == 8):
                ch_EN1 += str(quit)[:4]
                ch_EN2 = str(quit)[4:] + ch_EN2
            
                for channel in range(len(str(quit))):
                    if(str(quit)[channel] == "1"):
                        channels_EN += 1

                startup(int(ch_EN1, 2), int(ch_EN2, 2))
                write_addr(0x00)
                for dummy_enabled_index in range(2 * channels_EN):
                    data = get_readings()[:2]
                    data1 = int_to_bin8(data[0])
                    if(get_channel(data1[:4]) <= lowest):
                        lowest = get_channel(data1[:4])
                break;
            else:
                print "Input Error"
        except KeyboardInterrupt:
            gpio.output(7, False)
            gpio.cleanup()
            print ""
            exit()
        except Exception, e:
            print e
            pass
    while(str(quit).lower() != "q"):
        try:       
            print "ENABLE dac channels with voltage levels separated with ','" 
            quit = input("(Note that the position refers to the channel D->A, in order.)\n>> ")
            voltage = list(quit)
        except KeyboardInterrupt:
            gpio.output(7, False)
            gpio.cleanup()
            print ""
            exit()
        except:
            quit = None
 
        if(len(voltage) != 4 or quit == None):
            print "Input Error"
        else:
            cmd = 0x30
            temp_cmd1 = "{0:b}".format(cmd).zfill(8)[:4]
            for channel in range(len(voltage)):
                temp_cmd2 = "{0:b}".format(cmd).zfill(8)[4:]
                temp_cmd2_list = list(temp_cmd2)
                temp_cmd2_list[channel] = "1"
                temp_cmd2 = "".join(temp_cmd2_list)
                cmd_bits = temp_cmd1 + temp_cmd2
                cmd_int = int(cmd_bits, 2)
                ch_voltage = volt_to_int(voltage[channel])
                ch_voltage_bits = "{0:b}".format(ch_voltage).zfill(RES)
                
                voltage_bits_list = [ch_voltage_bits[i: i + 8] for i in range(0, len(ch_voltage_bits), 8)]
                
                while(len(voltage_bits_list[-1]) != 8):
                    voltage_bits_list[-1] += "1"

                ch_voltage_int = []               
                    
                try:
                    for voltage_bits in voltage_bits_list:
                        ch_voltage_int.append(int(voltage_bits, 2))
                    #print ADDRDAC, cmd_int, ch_voltage_int
                    bus.write_i2c_block_data(ADDRDAC, cmd_int, ch_voltage_int)
                except Exception, e:
                    print e

        if(lowest != 9):
            while(True):
                data = get_readings()[:2]
                data1 = int_to_bin8(data[0])
                data2 = int_to_bin8(data[1])
                if(get_channel(data1[:4]) == lowest):
                    print "CH" + str(get_channel(data1[:4])) + ": "
                    voltage_bin = data1[4:] + data2
                    print int_to_volt(int(voltage_bin, 2))
                    time.sleep(0.001)
                    break; 


            for dummy_enabled_index in range(1, channels_EN):
                data = get_readings()[:2]
                data1 = int_to_bin8(data[0])
                data2 = int_to_bin8(data[1])
                print "CH" + str(get_channel(data1[:4])) + ": "
                voltage_bin = data1[4:] + data2
                print int_to_volt(int(voltage_bin, 2))
                time.sleep(0.001)
                                                
except KeyboardInterrupt:
    gpio.output(7, False)
    gpio.cleanup()
    print ""
    exit()
