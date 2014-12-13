from seps525 import SEPS525_nhd as Oled
from template import Template_img as Temp
import time


t1 = time.time()
VIMeas1 = Temp("VIMeas1", "VIMeas1.csv")
VISet1 = Temp("VISet1", "VISet1.csv")
VMS1 = Temp("VMS1", "VMS1.csv")
IMS1 = Temp("IMS1", "IMS1.csv")
t2 = time.time()

print "INIT: " + str(t2 - t1)

TEMPS = {
    "VIMeas1" : VIMeas1.update_oled,
    "VISet1"  : VISet1.update_oled,
    "VMS1"    : VMS1.update_oled,
    "IMS1"    : IMS1.update_oled,
    }

display = Oled()
try:
    print "trying"
    display.show()
    display.fill_screen((255, 255))
    time.sleep(0.5)
    display.fill_screen((0,0))
    time.sleep(0.5)
    print "templates"
    TEMPS["VIMeas1"](display)
    time.sleep(0.5)
    TEMPS["VISet1"](display)
    time.sleep(0.5)
    TEMPS["VMS1"](display)
    time.sleep(0.5)
    TEMPS["IMS1"](display)
    time.sleep(0.5)
    print "done"
    display.hide()
    display.end_gpio()
except Exception, e:
    print e
    display.hide()
    display.end_gpio()
