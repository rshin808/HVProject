class SEPS525_nhd:
    # LIBRARIES
    import spidev
    import time
    import RPi.GPIO as gpio
    import csv
    from font import Font


    # PINS
    RES = 8
    RS = 12

    # ADDRESSES
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
    SCR2_FU = 0x40
    SCR2_MXY = 0x41
    MOV_DIR = 0x42
    SCR2_SX1 = 0x47
    SCR2_SX2 = 0x48
    SCR2_SY1 = 0x49
    SCR2_SY2 = 0x4A

    def __init__(self, WIDTH = 160, HEIGHT = 128, font = "font14h"):
	# Initialize gpio
	self.__setup_gpio()

	self._WIDTH = WIDTH
	self._HEIGHT = HEIGHT
	self._font = Font(font)
	self.__seps525_init()
	self.__init_oled()
	
    def __setup_gpio(self):
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

    def end_gpio(self):
	gpio.output(RES, True)
	gpio.cleanup()
	exit()

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
	seps525_reg(I_RED, 0x00)
	time.sleep(0.002)

	seps525_reg(SS_CNTRL, 0x00)

	# set EXPORT1 at internal clock
        seps525_reg(OSC, 0x01)

	# set framerate as 120 Hz
	seps525_reg(C_DIV, 0x30)

	# set reference voltage controlled by external resistor
	seps525_reg(I_REF, 0x01)

	# set pre-charge time
	# red
	seps525_reg(PRE_TR, 0x04)
	# green
	seps525_reg(PRE_TG, 0x05)
	# blue  
	seps525_reg(PRE_TB, 0x05)

	# set pre-charge current
	# red
	seps525_reg(PRE_CR, 0x9D)
	# green
	seps525_reg(PRE_CG, 0x8C)
	# blue
	seps525_reg(PRE_CB, 0x57)

	# set driving current
	# red
	seps525_reg(DRI_CR, 0x56)
	# green
	seps525_reg(DRI_CG, 0x4D)
	# blue 
	seps525_reg(DRI_CB, 0x46)

	# set color sequence
	seps525_reg(DISP_MODE, 0x00)
        
	# set MCU interface mode
	seps525_reg(RGB_IF, 0x01)
	seps525_reg(MEM_WM, 0x66)
    
	# shift mapping RAM counter
	seps525_reg(MEM_ACX, 0x00)
	seps525_reg(MEM_ACY, 0x00)

	# 1/128 duty
	seps525_reg(DUTY, 0x7F)

	# set mapping
	seps525_reg(DSL, 0x00)

	# display on
	seps525_reg(DISP_O_F, 0x01)

	# disable power save mode
	seps525_reg(S_RST, 0x00)

    	# set RGB polarity
	seps525_reg(RGB_POL, 0x00)

    def __init_oled_display(self):
	fill_screen((0, 0))

    def __seps525_set_region(self, width1 = 0, height1 = 0, width2 = 160, height2 = 128):
	# specify the update region
	# start on (width1, height1)
	seps525_reg(MX1, width1)
	seps525_reg(MX2, width1 + width2 - 1)
	seps525_reg(MX3, height1)
	seps525_reg(MX4, height1 + height2 -1)
	seps525_reg(MEM_ACX, width1)
	seps525_reg(MEM_ACY, height1)
    
    def __data(self, value):
	# send value
	gpio.output(RS, True)
	spi.xfer2(list(value))
	gpio.output(RS, False)
    
    def __data_start(self):
	gpio.output(RS, False)
	spi.xfer([0x22])
	gpio.output(RS, True)

    def seps525_reg(self, address, value):
	# goto index of address and set it to value
	gpio.output(RS, False)
	spi.xfer2([address])
	gpio.output(RS, True)
	spi.xfer2([value])

    def fill_screen(self, color):
	# color = (c1, c2)
	self.__seps525_set_region()
	self.__data_start()
	value = []
	
	# create array of 4096
	for pixel in range(2048):
	    value.append(color[0])
	    value.append(color[1])

	# send data 4096 bytes each 
	for pixel in range(10):
	    self.__data(value)

    def draw_pixel(self, x, y, color):
	# color = (c1, c2)
	self.__seps525_set_region(x, y, 1, 1)
	self.__data_start()
	self.__data(list(color))

    def draw_vline(self, x, y, h, color):
	# color = (c1, c2)
	self.__seps525_set_region(x, y, 1, h)
	self.__data_start()

	value = []
	for pixel in range(2 * h):
	    value.append(color[0])
	    value.append(color[1])
	
	self.__data(value)

    def draw_hline(self, x, y, w, color):
	# color = (c1, c2)
	self.__seps525_set_region(x, y, w, 1)
	self.__data_start()

	value = []
	for pixel in range(2 * w):
	    value.append(color[0])
	    value.append(color[1])

	self.__data(value)

    def draw_rect(self, x, y, w, h, color, filled = True):
	# color = (c1, c2)
	if(filled):
	    self.__set_region(x, y, w, h)
	    self.__data_start()
	    value = []
	    for pixel in range(2 * h * w):
		value.append(color[0])
		value.append(color[1])

	    self.__data(value)
	else:
	    self.draw_vline(x, y, h, color)
	    self.draw_hline(x, y, w, color)
	    self.draw_hline(x, y + h, color)
	    self.draw_vline(x + w, y, h, color)
    
    def draw_circle(self, x, y, r, color, filled = False):
	# color = (c1, c2)
	if(!filled):
	    self.draw_pixel(x, y - r, color)
	    self.draw_pixel(x, 2 * r + 1, color)
	    f = 1 - r
	    ddf_x = 1
	    ddr_y = -1 * r
	    x1 = 0
	    y1 = r
	    while (x1 < y1):
		if(f >= 0):
		    y1 -= 1
		    ddf_y += 2
		    f += ddf_y
		x1 += 1
		ddf_x += 2
		f += ddf_x

		self.draw_pixel((x + x1), (y - y1), color)
		self.draw_pixel((x + x1), (y + y1), color)
		self.draw_pixel((x + y1), (y - x1), color)
		self.draw_pixel((x + y1), (y + x1), color)
		self.draw_pixel((x - x1), (y - y1), color)
		self.draw_pixel((x - x1), (y + y1), color)
		self.draw_pixel((x - y1), (y - x1), color)
		self.draw_pixel((x - y1), (y + x1), color)
    
    def hide(self):
	seps525_reg(DISP_O_F, 0x00)
