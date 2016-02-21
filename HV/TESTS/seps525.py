import spidev
import time
import RPi.GPIO as gpio
import csv
from font import Font


class SEPS525_NHD:
    # ADDRESSES
    _INDEX = 0x00
    _STATUS = 0x01
    _OSC = 0x02
    _I_REF = 0x80
    _C_DIV = 0x03
    _I_RED = 0x04
    _S_RST = 0x05
    _DISP_O_F = 0x06
    _PRE_TR = 0x08
    _PRE_TG = 0x09
    _PRE_TB = 0x0A
    _PRE_CR = 0x0B
    _PRE_CG = 0x0C
    _PRE_CB = 0x0D
    _DRI_CR = 0x10
    _DRI_CG = 0x11
    _DRI_CB = 0x12
    _DISP_MODE = 0x13
    _RGB_IF = 0x14
    _RGB_POL = 0x15
    _MEM_WM = 0x16
    _MX1 = 0x17
    _MX2 = 0x18
    _MX3 = 0x19
    _MX4 = 0x1A
    _MEM_ACX = 0x20
    _MEM_ACY = 0x21
    _DDRAM = 0x22
    _GRAY_IDX = 0x50
    _GRAY_DATA = 0x51
    _DUTY = 0x28
    _DSL = 0x29
    _D1_FAC = 0x2E
    _D1_FAR = 0x2F
    _D2_SAC = 0x31
    _D2_SAR = 0x32
    _FX1 = 0x33
    _FX2 = 0x34
    _FY1 = 0x35
    _FY2 = 0x36
    _SX1 = 0x37
    _SX2 = 0x38
    _SY1 = 0x39
    _SY2 = 0x3A
    _SS_CNTRL = 0x3B
    _SS_ST = 0x3C
    _SS_MODE = 0x3D
    _SCR1_FU = 0x3E
    _SCR1_MXY = 0x3F
    _SCR2_FU = 0x40
    _SCR2_MXY = 0x41
    _MOV_DIR = 0x42
    _SCR2_SX1 = 0x47
    _SCR2_SX2 = 0x48
    _SCR2_SY1 = 0x49
    _SCR2_SY2 = 0x4A


    def __init__(self, WIDTH = 160, HEIGHT = 128, font = "font14h", font2 = "font14hL", DC = None, RES = None):
	    # Initialize gpio
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        self._font = Font(font)
        self._font2 = Font(font2)
        self._DC = DC
        self._RES = RES
	
    def setup_gpio(self, gpio, spi):
        gpio.setup(self._RES, gpio.OUT)
        gpio.output(self._RES, True)
        gpio.setup(self._DC, gpio.OUT)
        gpio.output(self._DC, False)
        time.sleep(0.1)
        
        spi.max_speed_hz = 80000000
        spi.mode = 3

    def end_gpio(self, gpio):
        gpio.output(self._RES, True)
        gpio.cleanup()

    def seps525_init(self, gpio):
        # Startup RS
        gpio.output(self._DC, False)
        time.sleep(0.5)
        gpio.output(self._DC, True)
        time.sleep(0.5)
    
        # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(self._I_RED, 0x01)
        time.sleep(0.002)

	    # Enable power save mode
	    # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(self._I_RED, 0x00)
        time.sleep(0.002)
        
        self.seps525_reg(self._SS_CNTRL, 0x00)

	    # set EXPORT1 at internal clock
        self.seps525_reg(self._OSC, 0x01)

	    # set framerate as 120 Hz
        self.seps525_reg(self._C_DIV, 0x30)

	    # set reference voltage controlled by external resistor
        self.seps525_reg(self._I_REF, 0x01)

	    # set pre-charge time
	    # red
        self.seps525_reg(self._PRE_TR, 0x04)
	    # green
        self.seps525_reg(self._PRE_TG, 0x05)
	    # blue  
        self.seps525_reg(self._PRE_TB, 0x05)

    	# set pre-charge current
	    # red
        self.seps525_reg(self._PRE_CR, 0x9D)
	    # green
        self.seps525_reg(self._PRE_CG, 0x8C)
	    # blue
        self.seps525_reg(self._PRE_CB, 0x57)

	    # set driving current
	    # red
        self.seps525_reg(self._DRI_CR, 0x56)
	    # green
        self.seps525_reg(self._DRI_CG, 0x4D)
	    # blue 
        self.seps525_reg(self._DRI_CB, 0x46)

	    # set color sequence
        self.seps525_reg(self._DISP_MODE, 0x00)
        
	    # set MCU interface mode
        self.seps525_reg(self._RGB_IF, 0x01)
        self.seps525_reg(self._MEM_WM, 0x66)
    
	    # shift mapping RAM counter
        self.seps525_reg(self._MEM_ACX, 0x00)
        self.seps525_reg(self._MEM_ACY, 0x00)

	    # 1/128 duty
        self.seps525_reg(self._DUTY, 0x7F)

	    # set mapping
        self.seps525_reg(self._DSL, 0x00)

	    # display on
        self.seps525_reg(self._DISP_O_F, 0x01)

	    # disable power save mode
        self.seps525_reg(self._S_RST, 0x00)

    	# set RGB polarity
        self.seps525_reg(self._RGB_POL, 0x00)

    def seps525_set_region(self, width1 = 0, height1 = 0, width2 = 160, height2 = 128):
	    # specify the update region
	    # start on (width1, height1)
        self.seps525_reg(self._MX1, width1)
        self.seps525_reg(self._MX2, width1 + width2 - 1)
        self.seps525_reg(self._MX3, height1)
        self.seps525_reg(self._MX4, height1 + height2 -1)
        self.seps525_reg(self._MEM_ACX, width1)
        self.seps525_reg(self._MEM_ACY, height1)
    
    def data(self, value, gpio, spi):
        # send value
        gpio.output(self._DC, True)
        spi.xfer2(list(value))
        gpio.output(self._DC, False)
    
    def data_start(self, gpio, spi):
        gpio.output(self._DC, False)
        spi.xfer([0x22])
        gpio.output(self._DC, True)

    def seps525_reg(self, address, value, gpio, spi):
        # goto index of address and set it to value
        gpio.output(self._DC, False)
        spi.xfer2([address])
        gpio.output(self._DC, True)
        spi.xfer2([value])

    def fill_screen(self, color, gpio, spi):
	    # color = (c1, c2)
        self.seps525_set_region()
        self.data_start(gpio, spi)
        value = []
	
	    # create array of 4096
        for pixel in range(2048):
            value.append(color[0])
            value.append(color[1])

	    # send data 4096 bytes each 
        for pixel in range(10):
	        self.data(value, gpio, spi)

    def draw_pixel(self, x, y, color, gpio, spi):
	    # color = (c1, c2)
	    self.seps525_set_region(x, y, 1, 1)
	    self.data_start(gpio, spi)
	    self.data(list(color), gpio, spi)

    def draw_vline(self, x, y, h, color, gpio, spi):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, 1, h)
        self.data_start(gpio, spi)
        value = []
        for pixel in range(h):
            value.append(color[0])
            value.append(color[1])
	
        self.data(value, gpio, spi)

    def draw_hline(self, x, y, w, color, gpio, spi):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, w, 1)
        self.data_start(gpio, spi)

        value = []
        for pixel in range(w):
            value.append(color[0])
            value.append(color[1])

        self.data(value, gpio, spi)

    def draw_rect(self, x, y, w, h, color, filled, gpio, spi):
	    # color = (c1, c2)
        if(filled):
            self.set_region(x, y, w, h)
            self.data_start(gpio, spi)
            value = []
            for pixel in range(2 * h * w):
                value.append(color[0])
                value.append(color[1])

            self.data(value, gpio, spi)
        else:
            self.draw_vline(x, y, h, color, gpio, spi)
            self.draw_hline(x, y, w, color, gpio, spi)
            self.draw_hline(x, y + h, color, gpio, spi)
            self.draw_vline(x + w, y, h, color, gpio, spi)
    
    def draw_circle(self, x, y, r, color, filled, gpio, spi):
	    # color = (c1, c2)
        if(not filled):
            self.draw_pixel(x, y - r, color, gpio, spi)
            self.draw_pixel(x, 2 * r + 1, color, gpio, spi)
            f = 1 - r
            ddf_x = 1
            ddr_y = -1 * r
            x1 = 0
            y1 = r
            while (x1 < y1):
                if(f >= 0):
                    y1 -= 1
                    ddf_y += 2
                f += ddf_x
                x1 += 1
                ddf_x += 2
                f += ddf_x
                self.draw_pixel((x + x1), (y - y1), color, gpio, spi)
                self.draw_pixel((x + x1), (y + y1), color, gpio, spi)
                self.draw_pixel((x + y1), (y - x1), color, gpio, spi)
                self.draw_pixel((x + y1), (y + x1), color, gpio, spi)
                self.draw_pixel((x - x1), (y - y1), color, gpio, spi)
                self.draw_pixel((x - x1), (y + y1), color, gpio, spi)
                self.draw_pixel((x - y1), (y - x1), color, gpio, spi)
                self.draw_pixel((x - y1), (y + x1), color, gpio, spi)
   
    def show(self):
        self.seps525_reg(DISP_O_F, 0x01)
     
    def hide(self):
        self.seps525_reg(DISP_O_F, 0x00)
