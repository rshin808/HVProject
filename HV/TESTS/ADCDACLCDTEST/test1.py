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

SPI = spi.SpiDev()
SPI.open(0, 0)
SPI.max_speed_hz = 100000000
SPI.mode = 3

font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")


gpio.setmode(gpio.BCM)
time.sleep(0.5)

display = SEPS525_NHD(DC = 24, RES = 25)
display.seps525_init(SPI, gpio)
display.fill_screen((255, 255), SPI, gpio)
IP = getIP()
loffset = 10
IPTitle = TS(loffset, 10, 14, "IP: ", font14h)
IPDisp = TS(loffset + len(IPTitle),10, 14, IP, font14h)
IPTitle.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
IPDisp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)

i2c = smbus.SMBus(1)

ch = int(0b00000011)

AD5696Functions["initAD5696"](["b", "d", "1"])
AD5696Functions["outputV"](["d", "0"])
AD5696Functions["outputV"](["b", "0"])
AD7998_1Functions["initAD7998_1"]([ch])
AD7998_1Functions["readADC"]([ch])


try:
    v = 0
    v2 = 4.98
    while(True):
        if v >= 4.98:
            v = 0
        else:
            v += 0.00625
        
        if v2 <= 0:
            v2 = 4.98
        else:
            v2 -= 0.00625

        i2c = smbus.SMBus(1)
        AD5696Functions["outputV"](["d", v])
        AD5696Functions["outputV"](["b", v2])
       
        reading = AD7998_1Functions["readADC"]([ch]) 
 
        print reading

        CH1Title = TS(loffset, 26, 14, "CH1: ", font14h)
        CH1Disp = TS(loffset + len(CH1Title),26, 14, str(reading[0]).rjust(4), font14h)
        CH1Title.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
        CH1Disp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
        
        CH2Title = TS(loffset, 42, 14, "CH2: ", font14h)
        CH2Disp = TS(loffset + len(CH2Title),42, 14, str(reading[1]).rjust(4), font14h)
        CH2Title.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
        CH2Disp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = gpio)
        
        time.sleep(0.005)
except KeyboardInterrupt, e:
    i2c.close()
    gpio.cleanup()
