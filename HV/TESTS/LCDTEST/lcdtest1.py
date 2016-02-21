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

font14hL = Font("font14hL")
font14hL.init_bitmap("font14hL.csv")

display = SEPS525_NHD(DC = 24, RES = 25)
display.seps525_init(SPI, GPIO)
display.fill_screen((255, 255), SPI, GPIO)
IP = getIP() 

loffset = 10
IPTitle = TS(loffset, 10, 14, "IP: ", font14h)
IPDisp = TS(loffset + len(IPTitle),10, 14, IP, font14h)
IPTitle.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)
IPDisp.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)


display.draw_rect(8, 24, 50, 18, (0, 0), False, spi = SPI, gpio = GPIO)
Test = TS(loffset, 26, 14, "0", font14hL)
Test2 = TS(loffset + len(Test), 26, 14, "0", font14hL)
Test3 = TS(loffset + len(Test) + len(Test2), 26, 14, "0", font14hL)
Test.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)
Test2.draw_string((255, 255), (0, 0), display, spi = SPI, gpio = GPIO)
Test3.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)

display.draw_rect(10, 60, 56, 18, (0, 0), False, spi = SPI, gpio = GPIO)
a = []
l = 0
for i in range(6):
    if i == 4:
        a.append(TS(12 + l, 62, 14, ".", font14hL))
    else:
        a.append(TS(12 + l, 62, 14, "0", font14hL))
    l += len(a[i])

print l
for i in a:
    i.draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO) 
try:
    i = 0
    while(1):
        if i == len(a):
            i = 0
        a[i].draw_string((255, 255), (0, 0), display, spi = SPI, gpio = GPIO)
        time.sleep(0.1)
        a[i].draw_string((0, 0), (255, 255), display, spi = SPI, gpio = GPIO)
        i += 1
except KeyboardInterrupt, e:
    print "Quiting"
    GPIO.cleanup()
    SPI.close()
