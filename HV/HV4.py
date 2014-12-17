from seps525 import SEPS525_nhd as Oled
from template import Template_img as Temp
from text import Text_string as TS
from ad7998_1 import AD7998_1 as ADC  
from ad5696 import AD5696 as DAC
from encoder2b import Encoder2b as Encoder
import time
import smbus
import RPi.GPIO as gpio

gpio.cleanup()
gpio.setmode(gpio.BOARD)

bus = smbus.SMBus(1)

display = Oled()

PINS = {
    "AS" : 11,
    "CONVST" : 10,
    "A1" : 18,
    "A0" : 22,
    "RESET" : 15,
    "LDAC" : 13,
    "ENCA" : 7,
    "ENCB" : 24,
    "ENCC" : 16,
}

VDefault = "0000.00"
IDefault = "0.00000"


CHV = ADC(PINS, 5, 12, 5, 0x23, "11111111")
VOUT = DAC(PINS, 5, 12, 0x0C, [0, 0, 0, 0])

CHV.init_adc_address(gpio)
VOUT.init_dac_address(gpio)

CHV.init_adc_bus(bus)

ENC = Encoder(PINS)
ENC.init_encoder(gpio)

class VIMeas(Temp):
    def __init__(self, name = "VIMeas", filename = "VIMeas.csv"):
        Temp.__init__(self, name, filename)
        self._current_pos = 0
        self._selection = ("Menu", "VISet", "1", "2", "3", "4")
        self._VD = []
        self._ID = []
        self._VD.append(TS(28, 50, 14, VDefault))
        self._VD.append(TS(28, 69, 14, VDefault))
        self._VD.append(TS(28, 88, 14, VDefault))
        self._VD.append(TS(28, 107, 14, VDefault))
        self._ID.append(TS(91, 50, 14, IDefault))
        self._ID.append(TS(91, 69, 14, IDefault))
        self._ID.append(TS(91, 88, 14, IDefault))
        self._ID.append(TS(91, 107, 14, IDefault))
        self._back = (175, 223)
        self._menu = (223, 60)
        self._line = [7, 18, 37] 
    def init(self, display):
        for V in self._VD:
            V.draw_string((0, 0), self._back, display)
        for I in self._ID:
            I.draw_string((0, 0), self._back, display)
  
    def update_pos(self, direction, display):
        prev = self._current_pos
        if direction == "LEFT":
            if self._current_pos <= 4:
                self._current_pos += 1
        else:
            if self._current_pos >= 1:
                self._current_pos -= 1
        print self._selection[self._current_pos]

        if self._current_pos == 0:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [7, 18, 30]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 1:
            if prev == 0:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._menu)
            elif prev == 2:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)

            self._line = [4, 40, 42]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 2:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 65, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 3:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 84, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 4:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 103, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        else:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 121, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
    def update_strings(self, adc, bus, display):
        adc.get_data(bus)
        c = 0
        half = 4
        limit = 8
        for v in adc:
            if c >= limit:
                break
            if c != -1:
                if c >= half:
                    self._ID[c - half].update_string(str(v)[:6])
                else:
                    self._VD[c].update_string(str(v)[:6])
                c += 1
        for c in range(half):
            self._VD[c].draw_string((0, 0), self._back, display)
            self._ID[c].draw_string((0, 0), self._back, display)
    def select_pos(self, display, check):
        global CURRENT
        CURRENT = SCREEN[self._selection[self._current_pos]]
        CURRENT.update_oled(display)


class VISet(Temp):
    def __init__(self, name = "VISet", filename = "VISet.csv"):
        Temp.__init__(self, name, filename)
        self._current_pos = 0
        self._selection = ("Menu", "VMS", "1", "2", "3", "4")
        self._VD = []
        self._ID = []
        self._VD.append(TS(28, 50, 14, VDefault))
        self._VD.append(TS(28, 69, 14, VDefault))
        self._VD.append(TS(28, 88, 14, VDefault))
        self._VD.append(TS(28, 107, 14, VDefault))
        self._ID.append(TS(91, 50, 14, IDefault))
        self._ID.append(TS(91, 69, 14, IDefault))
        self._ID.append(TS(91, 88, 14, IDefault))
        self._ID.append(TS(91, 107, 14, IDefault))
        self._back = (15, 233)
        self._menu = (223, 60)
        self._line = [7, 18, 37] 
    def init(self, display):
        for V in self._VD:
            V.draw_string((0, 0), self._back, display)
        for I in self._ID:
            I.draw_string((0, 0), self._back, display)
  
    def update_pos(self, direction, display):
        prev = self._current_pos
        if direction == "LEFT":
            if self._current_pos <= 4:
                self._current_pos += 1
        else:
            if self._current_pos >= 1:
                self._current_pos -= 1
        print self._selection[self._current_pos]

        if self._current_pos == 0:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [7, 18, 30]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 1:
            if prev == 0:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._menu)
            elif prev == 2:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)

            self._line = [33, 40, 34]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 2:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 62, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 3:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 81, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 4:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 100, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        else:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 119, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
    
    def update_strings(self, dac, bus, display):
        

    def select_pos(self, display, check):
        global CURRENT
        CURRENT = SCREEN[self._selection[self._current_pos]]
        CURRENT.update_oled(display)

class VMS(Temp):
    def __init__(self, name = "VMS", filename = "VMS.csv"):
        Temp.__init__(self, name, filename)
        self._current_pos = 0
        self._selection = ("Menu", "IMS", "1", "2", "3", "4")
        self._VM = []
        self._VS = []
        self._VM.append(TS(28, 50, 14, VDefault))
        self._VM.append(TS(28, 69, 14, VDefault))
        self._VM.append(TS(28, 88, 14, VDefault))
        self._VM.append(TS(28, 107, 14, VDefault))
        self._VS.append(TS(91, 50, 14, IDefault))
        self._VS.append(TS(91, 69, 14, IDefault))
        self._VS.append(TS(91, 88, 14, IDefault))
        self._VS.append(TS(91, 107, 14, IDefault))
        self._back = (246, 0)
        self._menu = (223, 60)
        self._line = [7, 18, 37] 
    def init(self, display):
        for V in self._VD:
            V.draw_string((0, 0), self._back, display)
        for I in self._ID:
            I.draw_string((0, 0), self._back, display)
  
    def update_pos(self, direction, display):
        prev = self._current_pos
        if direction == "LEFT":
            if self._current_pos <= 4:
                self._current_pos += 1
        else:
            if self._current_pos >= 1:
                self._current_pos -= 1
        print self._selection[self._current_pos]

        if self._current_pos == 0:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [7, 18, 30]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 1:
            if prev == 0:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._menu)
            elif prev == 2:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)

            self._line = [67, 40, 25]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 2:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 62, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 3:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 81, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 4:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 100, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        else:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 119, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
    def update_strings(self, adc, b00us, display):
        pass

    def select_pos(self, display, check):
        global CURRENT
        CURRENT = SCREEN[self._selection[self._current_pos]]
        CURRENT.update_oled(display)

class IMS(Temp):
    def __init__(self, name = "IMS", filename = "IMS.csv"):
        Temp.__init__(self, name, filename)
        self._current_pos = 0
        self._selection = ("Menu", "VIMeas", "1", "2", "3", "4")
        self._VD = []
        self._ID = []
        self._VD.append(TS(28, 50, 14, VDefault))
        self._VD.append(TS(28, 69, 14, VDefault))
        self._VD.append(TS(28, 88, 14, VDefault))
        self._VD.append(TS(28, 107, 14, VDefault))
        self._ID.append(TS(91, 50, 14, IDefault))
        self._ID.append(TS(91, 69, 14, IDefault))
        self._ID.append(TS(91, 88, 14, IDefault))
        self._ID.append(TS(91, 107, 14, IDefault))
        self._back = (249, 192)
        self._menu = (223, 60)
        self._line = [7, 18, 37] 
    def init(self, display):
        for V in self._VD:
            V.draw_string((0, 0), self._back, display)
        for I in self._ID:
            I.draw_string((0, 0), self._back, display)
  
    def update_pos(self, direction, display):
        prev = self._current_pos
        if direction == "LEFT":
            if self._current_pos <= 4:
                self._current_pos += 1
        else:
            if self._current_pos >= 1:
                self._current_pos -= 1
        print self._selection[self._current_pos]

        if self._current_pos == 0:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [7, 18, 30]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 1:
            if prev == 0:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._menu)
            elif prev == 2:
                display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
                
            self._line = [95, 40, 25]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 2:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 62, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 3:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 81, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        elif self._current_pos == 4:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 100, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
        else:
            display.draw_hline(self._line[0], self._line[1], self._line[2], self._back)
            self._line = [4, 119, 150]
            display.draw_hline(self._line[0], self._line[1], self._line[2], (0, 0))
    def update_strings(self, adc, bus, display):
        pass

    def select_pos(self, display, check):
        global CURRENT
        CURRENT = SCREEN[self._selection[self._current_pos]]
        CURRENT.update_oled(display)
VIMeas1 = VIMeas("VIMeas", "VIMeas1.csv")
VISet1 = VISet("VISet", "VISet1.csv")
VMS1 = VMS("VMS", "VMS1.csv")
IMS1 = IMS("IMS", "IMS1.csv")
SCREEN = {
    "VIMeas" : VIMeas1,
    "VISet" : VISet1,
    "VMS" : VMS1,
    "IMS" : IMS1,
    "Menu": VIMeas1,
    "VIMeasN": VIMeas1,
    "VISetN": VISet1,
    "VMSN" : VMS1,
    "IMSN" : IMS1,
}

CURRENT = SCREEN["VIMeas"]

try:
    display.show()
    display.fill_screen((0,0))
    time.sleep(0.5)
    CURRENT.update_oled(display)
    CURRENT.init(display)
    while(True):
        check = ENC.wait_hold(gpio)
        if check == False:
            CURRENT.select_pos(display, check)

        direction = ENC.get_direction(gpio)
        CURRENT.update_strings(CHV, bus, display)
        if direction != "SAME":
            CURRENT.update_pos(direction, display)
except KeyboardInterrupt:
    display.hide()
    display.end_gpio()
"""
except Exception, e:
    print e
    display.hide()
    display.end_gpio()
"""
