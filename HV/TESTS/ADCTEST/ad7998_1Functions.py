import smbus
import time
import RPi.GPIO as gpio
import sys

# Registers
CONV = 0x00
ALERT = 0x01
CONFIG = 0x02
CYCLE = 0x03
DATA_L1 = 0x04
DATA_H1 = 0x05
HYS1 = 0x06
DATA_L2 = 0x07
DATA_H2 = 0x08
HYS2 = 0x09
DATA_L3 = 0x0A
DATA_H3 = 0x0B
HYS3 = 0x0C
DATA_L4 = 0x0D
DATA_H4 = 0x0E
HYS4 = 0x0F

# Input

func = sys.argv[1]
params = []
for arg in range(1, len(sys.argv)):


def initAD7998_1(params):
    pass        

AD7998_1Functions = {
    "initAD7998_1" : initAD7998_1,
}



