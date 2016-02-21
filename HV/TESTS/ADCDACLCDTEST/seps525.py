"""
    File: seps525.py
    By  : Reed Shinsato
    Desc: This implements the class for the basic seps525 functions.
"""

# Libraries
import spidev
import time
import csv
from font import Font
from SEPS525REGS import *

# PINS
#RS = 31
#RES = 30

#RS =  24
#RES = 25


class SEPS525_NHD:
    """
        Constructor
        Param: WIDTH, The pixel width of the lcd.
               HEIGHT, The pixel height of the lcd.
               font, The font without spaces.
               font2, The font with spaces.
    """
    def __init__(self, DC = None, RES = None, WIDTH = 160, HEIGHT = 128):
	    # Initialize gpio
        self._DC = DC
        self._RES = RES
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        #self.__seps525_init()
        #self.__init_oled_display()

    """
        This sets the gpio (and spi) for the SEPS525 driver.
    """
    def __setup_gpio(self, spi = None, gpio = None):
        gpio.setup(self._RES, gpio.OUT)
        gpio.output(self._RES, True)
        gpio.setup(self._DC, gpio.OUT)
        gpio.output(self._DC, False)
        time.sleep(0.1)
        

    """
        This cleans up the gpio and turns off the SEPS525 driver.
    """
    def end_gpio(self, gpio = None):
        gpio.output(self._RES, True)
        gpio.cleanup()


    """
        This initializes the SEPS525 driver.
    """
    def seps525_init(self, spi = None, gpio = None):
        self.__setup_gpio(spi = spi, gpio = gpio)
        # Startup RS
        gpio.output(self._DC, False)
        time.sleep(0.5)
        gpio.output(self._DC, True)
        time.sleep(0.5)
    
        # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(I_RED, 0x01, spi, gpio)
        time.sleep(0.002)

	    # Enable power save mode
	    # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(I_RED, 0x00, spi, gpio)
        time.sleep(0.002)
        
        self.seps525_reg(SS_CNTRL, 0x00, spi, gpio)

	    # set EXPORT1 at internal clock
        self.seps525_reg(OSC, 0x01, spi, gpio)

	    # set framerate as 120 Hz
        self.seps525_reg(C_DIV, 0x30, spi, gpio)

	    # set reference voltage controlled by external resistor
        self.seps525_reg(I_REF, 0x01, spi, gpio)

	    # set pre-charge time
	    # red
        self.seps525_reg(PRE_TR, 0x04, spi, gpio)
	    # green
        self.seps525_reg(PRE_TG, 0x05, spi, gpio)
	    # blue  
        self.seps525_reg(PRE_TB, 0x05, spi, gpio)

    	# set pre-charge current
	    # red
        self.seps525_reg(PRE_CR, 0x9D, spi, gpio)
	    # green
        self.seps525_reg(PRE_CG, 0x8C, spi, gpio)
	    # blue
        self.seps525_reg(PRE_CB, 0x57, spi, gpio)

	    # set driving current
	    # red
        self.seps525_reg(DRI_CR, 0x56, spi, gpio)
	    # green
        self.seps525_reg(DRI_CG, 0x4D, spi, gpio)
	    # blue 
        self.seps525_reg(DRI_CB, 0x46, spi, gpio)

	    # set color sequence
        self.seps525_reg(DISP_MODE, 0x00, spi, gpio)
        
	    # set MCU interface mode
        self.seps525_reg(RGB_IF, 0x01, spi, gpio)
        self.seps525_reg(MEM_WM, 0x66, spi, gpio)
    
	    # shift mapping RAM counter
        self.seps525_reg(MEM_ACX, 0x00, spi, gpio)
        self.seps525_reg(MEM_ACY, 0x00, spi, gpio)

	    # 1/128 duty
        self.seps525_reg(DUTY, 0x7F, spi, gpio)

	    # set mapping
        self.seps525_reg(DSL, 0x00, spi, gpio)

	    # display on
        self.seps525_reg(DISP_O_F, 0x01, spi, gpio)

	    # disable power save mode
        self.seps525_reg(S_RST, 0x00, spi, gpio)

    	# set RGB polarity
        self.seps525_reg(RGB_POL, 0x00, spi, gpio)


    """
        This sets the region of the lcd to draw to.
        Param: width1, The starting pixel width point. 
               height1, The starting pixel height point.
               width2, The end pixel width point.
               height2, The end pixel height point.
    """
    def seps525_set_region(self, width1 = 0, height1 = 0, width2 = 160, height2 = 128, spi = None, gpio = None):
	    # specify the update region
	    # start on (width1, height1)
        self.seps525_reg(MX1, width1, spi, gpio)
        self.seps525_reg(MX2, width1 + width2 - 1, spi, gpio)
        self.seps525_reg(MX3, height1, spi, gpio)
        self.seps525_reg(MX4, height1 + height2 - 1, spi, gpio)
        self.seps525_reg(MEM_ACX, width1, spi, gpio)
        self.seps525_reg(MEM_ACY, height1, spi, gpio)
    

    """
        This writes data to the SEPS525 driver.
        It is mainly for writing the pixel color data.
        Param: value, The data to write.
    """
    def data(self, value = 0, spi = None, gpio = None):
        # send value
        gpio.output(self._DC, True)
        spi.xfer2(list(value))
        gpio.output(self._DC, False)
    

    """
        This writes the command address of display for the SEPS525 driver.
    """
    def data_start(self, spi = None, gpio = None):
        gpio.output(self._DC, False)
        spi.xfer([0x22])
        gpio.output(self._DC, True)

    
    """
        This writes a value to a specified register address of the SEPS525 driver.
        Param: address, The address of the register.
               value, The value to write to the register.
    """
    def seps525_reg(self, address = None, value = 0, spi = None, gpio = None):
        # goto index of address and set it to value
        gpio.output(self._DC, False)
        spi.xfer2([address])
        gpio.output(self._DC, True)
        spi.xfer2([value])

    
    """
        This fills the entire screen of the lcd with a color.
        Param: color, The color to fill the screen with. 
    """
    def fill_screen(self, color = (0, 0), spi = None, gpio = None):
	    # color = (c1, c2)
        self.seps525_set_region(spi = spi, gpio = gpio)
        self.data_start(spi = spi, gpio = gpio)
        value = []
	
	    # create array of 4096
        for pixel in range(2048):
            value.append(color[0])
            value.append(color[1])

	    # send data 4096 bytes each 
        for pixel in range(10):
	        self.data(value, spi = spi, gpio = gpio)


    """
        This draws a pixel to the lcd.
        Param: x, The x coordinate of the pixel.
               y, The y coordinate of the pixel.
               color, The color of the pixel.
    """
    def draw_pixel(self, x = 0, y = 0, color = (0, 0), spi = None, gpio = None):
	    # color = (c1, c2)
	    self.seps525_set_region(x, y, 1, 1, spi = spi, gpio = gpio)
	    self.data_start(spi = spi, gpio = gpio)
	    self.data(list(color), spi = spi, gpio = gpio)

    
    """
        This draws a vertical line to the lcd.
        Param: x, The start x coordinate of the line.
               y, The start y coordinate of the line.
               h, The height of the line.
               color, The color of the line.
    """
    def draw_vline(self, x = 0, y = 0, h = 0, color = (0, 0), spi = None, gpio = None):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, 1, h + 1, spi = spi, gpio = gpio)
        self.data_start(spi = spi, gpio = gpio)
        value = []
        for pixel in range(h + 1):
            value.append(color[0])
            value.append(color[1])
	
        self.data(value, spi = spi, gpio = gpio)


    """
        This draws a horizontal line to the lcd.
        Param: x, The start x coordinate of the line.
               y, The start y coordinate of the line.
               w, The width of the line.
               color, The color of the line.
    """
    def draw_hline(self, x = 0, y = 0, w = 0, color = (0, 0), spi = None, gpio = None):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, w + 1, 1, spi = spi, gpio = gpio)
        self.data_start(spi = spi, gpio = gpio)

        value = []
        for pixel in range(w + 1):
            value.append(color[0])
            value.append(color[1])

        self.data(value, spi = spi, gpio = gpio)


    """
        This draws a rectangle on the lcd.
        Param: x, The start x coordinate of the rectangle.
               y, The start y coordinate of the rectangle.
               w, The width of the rectangle.
               h, The height of the rectangle.
               color, The color of the rectangle.
               filled, Whether the rectangle is filled or not.
    """
    def draw_rect(self, x = 0, y = 0, w = 0, h = 0, color = (0, 0), filled = True, spi = None, gpio = None):
	    # color = (c1, c2)
        if(filled):
            self.set_region(x, y, w, h, spi = spi, gpio = gpio)
            self.data_start(spi = spi, gpio = gpio)
            value = []
            for pixel in range(2 * h * w):
                value.append(color[0])
                value.append(color[1])

            self.data(value, spi = spi, gpio = gpio)
        else:
            self.draw_vline(x, y, h, color, spi = spi, gpio = gpio)
            self.draw_hline(x, y, w, color, spi = spi, gpio = gpio)
            self.draw_hline(x, y + h, w, color, spi = spi, gpio = gpio)
            self.draw_vline(x + w, y, h, color, spi = spi, gpio = gpio)
    
    
    """
        This draws a circle to the lcd.
        Param: x, The x origin of the circle.
               y, The y origin of the circle.
               r, The radius of the circle.
               color, The color of the circle.
               filled, Whether the circle is filled or not.
    """
    def draw_circle(self, x, y, r, color, filled = False, spi = None, gpio = None):
	    # color = (c1, c2)
        if(not filled):
            self.draw_pixel(x, y - r, color, spi = spi, gpio = gpio)
            self.draw_pixel(x, 2 * r + 1, color, spi = spi, gpio = gpio)
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
                self.draw_pixel((x + x1), (y - y1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x + x1), (y + y1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x + y1), (y - x1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x + y1), (y + x1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x - x1), (y - y1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x - x1), (y + y1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x - y1), (y - x1), color, spi = spi, gpio = gpio)
                self.draw_pixel((x - y1), (y + x1), color, spi = spi, gpio = gpio)
   

    """
        This tells the SEPS525 driver to turn on the display.
    """
    def show(self, spi = None, gpio = None):
        self.seps525_reg(DISP_O_F, 0x01, spi = spi, gpio = gpio)
     

    """
        This tells the SEPS525 driver to turn off the display.
    """
    def hide(self, spi = None, gpio = None):
        self.seps525_reg(DISP_O_F, 0x00, spi = spi, gpio = gpio)

