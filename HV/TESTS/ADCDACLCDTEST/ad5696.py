import time

class AD5696:
    def __init__(self, RESET = None, VREF = 5, RES = 16, ADDRESS = 0x0C, voltages = [0, 0, 0, 0]):
        self._RESET = RESET
        self._VREF = VREF
        self._RES = RES
        self._ADDRESS = ADDRESS
        self._voltages = voltages
        self._enabled = None
        

    def __str__(self):
        return

    def __iter__(self):
        return

    def init_dac_address(self, gpio = None):
        gpio.setup(self._RESET, gpio.OUT)
        gpio.output(self._RESET, True)
        time.sleep(0.001)
    
    def update_voltage(self, channel = None, voltage = None):
        self._voltages[channel] = voltage

    def update_voltages(self, voltages = [0, 0, 0, 0]):
        self._voltages = voltages
    
    def __voltage_to_int(self, voltage = 0):
        conversion = 2 ** self._RES - 1
        scalar = float(conversion) / float(self._VREF)
        return int(voltage * scalar)

    def configure_enabled(self, power_down = 0, channels_enabled = [0, 0, 0, 0], i2c = None):
        """
            Function:   configure_enabled
            
            Desc:       This powers down the outputs that are not enabled.
                        
            Params:     power_down (integer), the mode.
                            0 (0x0) :    Normal Operation
                            1 (0x1) :    1kOhm-to-GND
                            2 (0x2) :    100kOhm-to-GND
                            3 (0x3) :    Three-State (High Impedance)
        
                        channels_enabled (list), the enabled channels.
                            0:  OFF
                            1:  ON
                            
                            Note: 0 for A ... 3 for D                        

                        i2c (object), the i2c handler.
        """
        cmd = 0x40
        pd = 0x00
        cmd_enabled = 0x0
        

        if channels_enabled[0] == 1:
            mask = 0x0 | 0x1
            cmd_enabled |= mask
        else:
            mask = 0x0 | 0x1
            mask = ~mask
            cmd_enabled &= mask
            pd |= power_down            

        if channels_enabled[1] == 1:
            mask = 0x0 | 0x2
            cmd_enabled |= mask
        else:
            mask = 0x0 | 0x2
            mask = ~mask 
            cmd_enabled &= mask
            pd |= (power_down << 2)            

        if channels_enabled[2] == 1:
            mask = 0x0 | 0x4
            cmd_enabled |= mask
        else:
            mask = 0x0 | 0x4
            mask = ~mask
            cmd_enabled &= mask
            pd |= (power_down << 4)            

        if channels_enabled[3] == 1:
            mask = 0x0 | 0x8
            cmd_enabled |= mask                
        else:
            mask = 0x0 | 0x8
            mask = ~mask
            cmd_enabled &= mask
            pd |= (power_down << 6)            

        self._enabled = cmd_enabled
        data = [0x00, pd]
        i2c.write_i2c_block_data(self._ADDRESS, cmd, data)

    """
        The channel voltage first needs to be set.
    """
    def output_voltage(self, i2c = None, channel = None):
        cmd = 0x30
        ch = 0
        if channel == 0 and (self._enabled & 0x1) == 1:
            cmd = cmd & 0xf1
            voltage = self._voltages[channel]
            data = [(voltage >> 8) & 0xff, voltage & 0xff]
            i2c.write_i2c_block_data(self._ADDRESS, cmd, data)
            
        elif channel == 1 and (self._enabled & 0x2) == 0x2:
            cmd = cmd & 0xf2
            voltage = self._voltages[channel]
            data = [(voltage >> 8) & 0xff, voltage & 0xff]
            i2c.write_i2c_block_data(self._ADDRESS, cmd, data)

        elif channel == 2 and (self._enabled & 0x4) == 0x4:
            cmd = cmd & 0xf4
            voltage = self._voltages[channel]
            data = [(voltage >> 8) & 0xff, voltage & 0xff]
            i2c.write_i2c_block_data(self._ADDRESS, cmd, data)

        elif channel == 3 and (self._enabled & 0x8) == 0x8:
            cmd = cmd & 0xf8
            voltage = self._voltages[channel]
            data = [(voltage >> 8) & 0xff, voltage & 0xff]
            i2c.write_i2c_block_data(self._ADDRESS, cmd, data)
        
    def output_voltages(self, i2c = None):
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
                i2c.write_i2c_block_data(self._ADDRESS, cmd_int, ch_voltages_int)
            except Exception, e:
                print e
