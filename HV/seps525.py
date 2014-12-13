import spidev
import time
import RPi.GPIO as gpio
import math
import Image
import os
import csv
import font

# PINS
RES = 8
RS = 12

def setup_gpio():
    global spi
    gpio.setmode(gpio.BOARD)
    gpio.setup(RES, gpio.OUT)
    gpio.output(RES, True)
    gpio.setup(RS, gpio.OUT)
    gpio.output(RS, False)
    time.sleep(0.1)
    
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 100000000
    spi.mode = 3


class seps525_nhd:
    INDEX = 0x00
    STATUS = 0x01
    OSC = 0x02
    I_REF = 0x80
    C_DIV = 0x03
    I_RED = 0x04
    S_RST = 0x05
    DISP_O_F = 0x06
    PRE_TR = 0x08
    PRE_TG = 0x09
    PRE_TB = 0x0A
    PRE_CR = 0x0B
    PRE_CG = 0x0C
    PRE_CB = 0x0D
    DRI_CR = 0x10
    DRI_CG = 0x11
    DRI_CB = 0x12
    DISP_MODE = 0x13
    RGB_IF = 0x14
    RGB_POL = 0x15
    MEM_WM = 0x16
    MX1 = 0x17
    MX2 = 0x18
    MX3 = 0x19
    MX4 = 0x1A
    MEM_ACX = 0x20
    MEM_ACY = 0x21
    DDRAM = 0x22
    GRAY_IDX = 0x50
    GRAY_DATA = 0x51
    DUTY = 0x28
    DSL = 0x29
    D1_FAC = 0x2E
    D1_FAR = 0x2F
    D2_SAC = 0x31
    D2_SAR = 0x32
    FX1 = 0x33
    FX2 = 0x34
    FY1 = 0x35
    FY2 = 0x36
    SX1 = 0x37
    SX2 = 0x38
    SY1 = 0x39
    SY2 = 0x3A
    SS_CNTRL = 0x3B
    SS_ST = 0x3C
    SS_MODE = 0x3D
    SCR1_FU = 0x3E
    SCR1_MXY = 0x3F
    SCR2_FU = x40
    SCR2_MXY = 0x41
    MOV_DIR = 0x42
    SCR2_SX1 = 0x47
    SCR2_SX2 = 0x48
    SCR2_SY1 = 0x49
    SCR2_SY2 = 0x4A

    def __init__(self, WIDTH = 160, HEIGHT = 128):
	# Initialize gpio
	setup_gpio()

	self._WIDTH = WIDTH
	self._HEIGHT = HEIGHT
	
	self.__seps525_init()

    def __seps525_init(self):
	# Startup RS
	gpio.output(RS, False)
	time.sleep(0.5)
	gpio.output(RS, True)
	time.sleep(0.5)
    
	# Set normal driving current
	# Disable oscillator power down
	spes525_reg(I_RED, 0x01)
	time.sleep(0.002)

	# Enable power save mode
	# Set normal driving current
	# Disable oscillator power down
	 seps525_reg(0x04, 0x00)
	time.sleep(0.002)

	seps525_reg(0x3B, 0x00)

	# set EXPORT1 at internal clock
     seps525_reg(0x02, 0x01)

	# set framerate as 120 Hz
	seps525_reg(0x03, 0x30)

	# set reference voltage controlled by external resistor
	seps525_reg(0x80, 0x01)

	# set pre-charge time
	# red
	seps525_reg(0x08, 0x04)
	# green
	seps525_reg(0x09, 0x05)
	# blue  
	seps525_reg(0x0A, 0x05)

	# set pre-charge current
	# red
	seps525_reg(0x0B, 0x9D)
	# green
	seps525_reg(0x0C, 0x8C)
	# blue
	seps525_reg(0x0D, 0x57)

	# set driving current
	# red
	seps525_reg(0x10, 0x56)
	# green
	seps525_reg(0x11, 0x4D)
	# blue 
	seps525_reg(0x12, 0x46)

	# set color sequence
	seps525_reg(0x13, 0x00)
        
	# set MCU interface mode
	seps525_reg(0x14, 0x01)
	seps525_reg(0x16, 0x66)
    
	# shift mapping RAM counter
	seps525_reg(0x20, 0x00)
	seps525_reg(0x21, 0x00)

	# 1/128 duty
	seps525_reg(0x28, 0x7F)

	# set mapping
	seps525_reg(0x29, 0x00)

	# display on
	seps525_reg(0x06, 0x01)

	# disable power save mode
	seps525_reg(0x05, 0x00)

    	# set RGB polarity
	seps525_reg(0x15, 0x00)

