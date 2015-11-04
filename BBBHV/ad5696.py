import smbus
import time
import RPi.GPIO as gpio

class AD5696:
    def __init__(self, PINS, VREF = 5, RES = 12, ADDRESS = 0x0C, voltages = [0, 0, 0, 0]):
        self._RESET = PINS["RESET"]
        self._A1 = PINS["A1"]
        self._A0 = PINS["A0"]
        self._LDAC = PINS["LDAC"]
        self._VREF = VREF
        self._RES = RES
        self._ADDRESS = ADDRESS
        self._voltages = voltages

    def __str__(self):
        return

    def __iter__(self):
        return

    def init_dac_address(self, gpio):
        gpio.setup(self._RESET, gpio.OUT)
        gpio.setup(self._A1, gpio.OUT)
        gpio.setup(self._A0, gpio.OUT)
        gpio.setup(self._LDAC, gpio.OUT)
        
        if self._ADDRESS == 0x0D:
            gpio.output(self._A1, False)
            gpio.output(self._A0, True)
        elif self._ADDRESS == 0x0E:
            gpio.output(self._A1, True)
            gpio.output(self._A0, False)
        elif self._ADDRESS == 0x0F:
            gpio.output(self._A1, True)
            gpio.output(self._A0, True)
        else:
            gpio.output(self._A1, False)
            gpio.output(self._A0, False)
        
        gpio.output(self._LDAC, False)
        gpio.output(self._RESET, True)
        time.sleep(0.001)

    def update_voltages(self, voltages = [0, 0, 0, 0]):
        self._voltages = voltages
    
    def __voltage_to_int(self, voltage):
        conversion = 2 ** self._RES - 1
        scalar = float(conversion) / float(self._VREF)
        return int(voltage * scalar)

    def output_voltages(self, bus):
        cmd = 0x30
        temp_cmd1 = "{0:b}".format(cmd).zfill(8)[:4]
        for channel in range(len(self._voltages)):
            temp_cmd2 = "{0:b}".format(cmd).zfill(8)[4:]
            temp_cmd2_list = list(temp_cmd2)
            temp_cmd2_list[channel] = "1"
            temp_cmd2 = "".join(temp_cmd2_list)
            cmd_bits = temp_cmd1 + temp_cmd2
            cmd_int = int(cmd_bits, 2)
            ch_voltages = self.__voltage_to_int(self._voltages[channel])
            ch_voltages_bits = "{0:b}".format(ch_voltages).zfill(self._RES)

            voltages_bits_list = [ch_voltages_bits[i: i + 8] for i in range(0, len(ch_voltages_bits), 8)]
            while(len(voltages_bits_list[-1]) != 8):
                voltages_bits_list[-1] += "1"

            ch_voltages_int = []

            try:
                for voltage_bits in voltages_bits_list:
                    ch_voltages_int.append(int(voltage_bits, 2))
                bus.write_i2c_block_data(self._ADDRESS, cmd_int, ch_voltages_int)
            except:
                pass
