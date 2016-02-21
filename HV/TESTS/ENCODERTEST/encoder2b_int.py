"""
    File: encoder2b.py
    By  : Reed Shinsato
    Desc: This implements the class for the encoder.
"""

# Libraries
import RPi.GPIO as gpio
import time

PINS = {
    "ENCA" : 7,
    "ENCB" : 23,
    "ENCC" : 22,
}

class Encoder2b:
    """
        Constructor
        Param: PINS, The pins of the encoder.
    """
    def __init__(self, PINS):
        self._ENCA = int(PINS["ENCA"])
        self._ENCB = int(PINS["ENCB"])
        self._ENCC = int(PINS["ENCC"])
        self._state = 0

    """
        This initializes the encoder.
        Param: gpio, The Raspberry Pi gpio object.
    """
    def initEncoder(self, gpio):
        gpio.setup(self._ENCA, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(self._ENCB, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(self._ENCC, gpio.IN, pull_up_down = gpio.PUD_UP)
        gpio.add_event_detect(self._ENCC, gpio.FALLING, bouncetime = 1)
        gpio.add_event_detect(self._ENCA, gpio.BOTH, bouncetime = 1)
        self.getState(gpio)

    def getState(self, gpio):
        a = int(gpio.input(self._ENCA))
        b = int(gpio.input(self._ENCB)) 
        self._state = ((a << 1) | b) & 0x3

    def __getState(self, gpio, A, B):
        if(A == True and B == False):
            return 2
        elif(A == False and B == True):
            return 1 
        else:
            return 0

    
    """
        This determines how long the encoder button has been held.
        Param: gpio, The Raspberry Pi gpio object.  
    """
    def waitHold(self, gpio):       
        if(gpio.event_detected(self._ENCC) == True):
            start = time.time()
            while(gpio.input(self._ENCC) == False):
                pass
            end = time.time()
            
            if float(end - start) >= 0.1 and float(end - start) < 0.6:
                time.sleep(0.01)
                return False
            elif float(end - start) >= 0.6:
                time.sleep(0.01)
                return True
            else:
                return None
        
        return None            

    """
        This gets the direction that the encoder was turned.
        Param: gpio, The Raspberry Pi gpio object.
    """
    def getDirection(self, gpio):
        if(gpio.event_detected(self._ENCA) == True):
            table = [0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 0]
            currentState = self._state
            self.getState(gpio)
            nextState = self._state
            
            index = ((currentState << 2) & 0xc) | (nextState & 0x3)
            if table[index] == 0:
                return None
            else:
                return table[index]
                    
    
        return None
