#!/usr/bin/python
# This simply sets all the output high

import smbus
import time
import RPi.GPIO as GPIO

#24 for !CONV
#23 for ALERT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, True)
time.sleep(0.5)

GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)
time.sleep(0.5)


bus = smbus.SMBus(1)

ADDR = 0x0C

VREF = 5
RES = 12

def convert_voltage_to_int(voltage):
    conversion = 2**RES - 1
    scalar = float(conversion) / float(VREF)
    return int(voltage * scalar)

try:
    quit = ""
    voltage = []
    while(str(quit).lower() != "q"):
        try:	
            quit = input("(Note that the position refers to channel D->A, in order.)\n >> ")        
            voltage = list(quit)
        except KeyboardInterrupt:
            GPIO.cleanup()
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
                ch_voltage = convert_voltage_to_int(voltage[channel])
                ch_voltage_bits = "{0:b}".format(ch_voltage).zfill(RES)
               
                voltage_bits_list = [ch_voltage_bits[i: i + 8] for i in range(0, len(ch_voltage_bits), 8)]
                
                while(len(voltage_bits_list[-1]) != 8):
                    voltage_bits_list[-1] += "1"

                ch_voltage_int = []
                try:
                    for voltage_bits in voltage_bits_list:
                        ch_voltage_int.append(int(voltage_bits, 2))
                    print ADDR, cmd_int, ch_voltage_int
                    bus.write_i2c_block_data(ADDR, cmd_int, ch_voltage_int)
                except Exception, e:
                    print e 

except KeyboardInterrupt:
    GPIO.cleanup()
    print ""
