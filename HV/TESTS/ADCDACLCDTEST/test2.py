import smbus
import RPi.GPIO as gpio
import time
from ad7998_1Functions import *
from ad5696Functions import *
import csv
from seps525 import *
from getIP import *
from text import Text_string as TS
import spidev as spi
from box import *
from page import *
from encoder2b_int import *

SPI = spi.SpiDev()
SPI.open(0, 0)
SPI.max_speed_hz = 100000000
SPI.mode = 3

i2c = smbus.SMBus(1)

font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")


gpio.setmode(gpio.BCM)
time.sleep(0.5)

display = SEPS525_NHD(DC = 24, RES = 25)
display.seps525_init(SPI, gpio)
display.fill_screen((255, 255), SPI, gpio)

home = Page(getIP(), Box1("Channel 1", 0, 0, font14h, (255, 255), (0, 0), 10, 26, 1), Box1("Channel 2", 0, 0, font14h, (255, 255), (0, 0), 10, 80, 2))

# Screen will cycle through pages
PAGES = [home]
currentPage = 0
CH1V = 0.0
CH2V = 0.0

# IP Address covers (10,10) to (10, 26) Height
# There are 2 pixels as spacers
"""
IP = getIP()
loffset = 10
IPTitle = TS(loffset, 10, 14, "IP: ", font14h)
IPDisp = TS(loffset + len(IPTitle),10, 14, IP, font14h)
IPTitle.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
IPDisp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
"""
# These are checking the output of the DAC
ch = int(0b00000011)

AD5696Functions["initAD5696"](["b", "d", "1"])
AD5696Functions["outputV"](["d", "0"])
AD5696Functions["outputV"](["b", "0"])
AD7998_1Functions["initAD7998_1"]([ch])
AD7998_1Functions["readADC"]([ch])

ENC = Encoder2b(PINS)
ENC.initEncoder(gpio)
ENC.getState(gpio)



try:
    PAGES[currentPage].drawPage(display, SPI, gpio, font14h)
    
    checkTime = time.time()
 
    while(True):
        check = ENC.waitHold(gpio)
        direction = ENC.getDirection(gpio)

        if check != None:
            nextPage = PAGES[currentPage].updateCheck(check)
            if nextPage != None:
                currentPage = nextPage

        if direction != None:
            PAGES[currentPage].updateDirection(direction)
    
        readings = AD7998_1Functions["readADC"]([ch])

        now = time.time()

        if PAGES[currentPage].getBox(1) == True and (now - checkTime) >= 0.005:
            x = None
            params = [x, x, x, x, readings[0], 5.0]
            PAGES[currentPage].updateBox(1, params)
            PAGES[currentPage].drawBox(1, [display, SPI, gpio])

        if PAGES[currentPage].getBox(2) == True and (now - checkTime) >= 0.005:
            x = None
            params = [x, x, x, x, readings[1], 5.0]
            PAGES[currentPage].updateBox(2, params)
            PAGES[currentPage].drawBox(2, [display, SPI, gpio])    
        
        if (now - checkTime) >= 0.005:
            checkTime = time.time()
except KeyboardInterrupt, e:
    i2c.close()
    gpio.cleanup()
