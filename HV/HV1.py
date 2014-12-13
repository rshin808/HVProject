from seps525 import SEPS525_nhd as Oled
from template import Template_img as Temp
import time

VIMeas1 = Temp("VIMeas1", "VIMeas1.csv")
VISet1 = Temp("VISet1", "VISet1.csv")
VMS1 = Temp("VMS1", "VMS1.csv")
IMS1 = Temp("IMS1", "IMS1.csv")

TEMPS = {
    "VIMeas1" : VIMeas1.update_oled,
    "VISet1"  : VISet1.update_oled,
    "VMS1"    : VMS1.update_oled,
    "IMS1"    : IMS1.update_oled,
    }

display = Oled()
try:
    display.fill_screen(255, 255)
    time.sleep(0.01)
    display.fill_screen(0,0)
    time.sleep(0.01)
except:
    display.hide()
    display.end_gpio()
