import spidev as spi
import RPi.GPIO as GPIO
import csv
from font import Font
from seps525 import *
from getIP import *
from text import Text_string as TS

GPIO.setmode(GPIO.BCM)
SPI = spi.SpiDev()
SPI.open(0, 0)
SPI.max_speed_hz = 100000000
SPI.mode = 3

font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")

display = SEPS525_NHD(DC = 24, RES = 25)
display.seps525_init(SPI, GPIO)
display.fill_screen((255, 255), SPI, GPIO)
IP = getIP() 

loffset = 10
IPTitle = TS(loffset, 10, 14, "IP: ", font14h)
IPDisp = TS(loffset + len(IPTitle),10, 14, IP, font14h)
IPTitle.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)
IPDisp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)
try:
    while(1):
        pass
except KeyboardInterrupt, e:
    print "Quiting"
    GPIO.cleanup()
    SPI.close()
