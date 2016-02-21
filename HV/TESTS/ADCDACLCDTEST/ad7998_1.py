import smbus
import time
import RPi.GPIO as gpio
from AD7998_1REGS import *


class AD7998_1:
    def __init__(self, CONVST = None, VREF = 5, RES = 12, VMAX = 5, ADDRESS = 0x20, CHANNELS = "11111111"):
        # PINS is a dictionary
        self._CONVST = CONVST 
        self._ADDRESS = ADDRESS
        self._RES = RES
        self._VREF = VREF
        self._VMAX = VMAX
        self._CHANNELS = CHANNELS
        self._channels_EN = 0
        self._lowest = 9
        self._voltage = [-1, -1, -1, -1, -1, -1, -1, -1]       

    def __str__(self):
        return 

    def __iter__(self):
        for v in self._voltage:
            yield v

    def __len__(self):
        return len(self._voltage)

    def init_adc(self, gpio = None):
        gpio.setup(self._CONVST, gpio.OUT)

        gpio.output(self._CONVST, True)
        time.sleep(0.1)

    def init_adc_bus(self, i2c = None, gpio = None):
        ch_EN1 = "0000"
        ch_EN2 = "1000"

        ch_EN1 += self._CHANNELS[:4]
        ch_EN2 = self._CHANNELS[4:] + ch_EN2

        for c in self._CHANNELS:
            if c == "1":
                self._channels_EN += 1

        self.__startup(i2c, int(ch_EN1, 2), int(ch_EN2, 2))
        self.__write_addr(i2c, CONV)

        for dummy_index in range(2 * self._channels_EN):
            data = self.get_readings(i2c, gpio)[:2]
            data1 = self.__int_to_bin8(data[0])
            if(self.get_channel(data1[:4]) < self._lowest):
                self._lowest = self.get_channel(data1[:4])
 
    def __write_addr(self, i2c = None, cmd = None):
        i2c.write_byte(self._ADDRESS, cmd)

    def __write_single_byte(self, i2c = None, cmd = None, data = None):
        i2c.write_i2c_block_data(self._ADDRESS, cmd, [data])

    def __write_two_byte(self, i2c = None, cmd = None, data1 = None, data2 = None):
        i2c.write_i2c_block_data(self._ADDRESS, cmd, [data1, data2])

    def __startup(self, i2c = None, cmd1 = None, cmd2 = None):
        self.__write_two_byte(i2c, CONFIG, cmd1, cmd2)
        self.__write_addr(i2c, CONV)   
 
    def __int_to_bin8(self, in_int = 0):
        return ("{0:b}".format(in_int).zfill(8))

    def __int_to_volt(self, in_int = 0):
        return ((float(in_int) / float(2 ** self._RES)) * float(self._VMAX))

    def get_channel(self, bin_string = ""):
        return int(bin_string[-3:], 2) + 1

    def get_readings(self, i2c = None, gpio = None):
        gpio.output(self._CONVST, False)
        time.sleep(0.01)
        gpio.output(self._CONVST, True)
        time.sleep(0.01)
        return i2c.read_i2c_block_data(self._ADDRESS, CONV)
    

    """
        This is the main method for getting ADC readings.
    """
    def get_data(self, i2c = None, gpio = None):
        flag = False
        while(flag == False):
            data = self.get_readings(i2c, gpio)[:2]
            data1 = self.__int_to_bin8(data[0])
            data2 = self.__int_to_bin8(data[1])
            if(self.get_channel(data1[:4]) == self._lowest):
                voltage_bin = data1[4:] + data2
                self._voltage[self.get_channel(data1[:4]) - 1] = self.__int_to_volt(int(voltage_bin, 2))
                flag = True
        for dummy_index in range(1, self._channels_EN):
            data = self.get_readings(i2c, gpio)[:2]
            data1 = self.__int_to_bin8(data[0])
            data2 = self.__int_to_bin8(data[1])
            voltage_bin = data1[4:] + data2
            self._voltage[self.get_channel(data1[:4]) - 1] = self.__int_to_volt(int(voltage_bin, 2))
