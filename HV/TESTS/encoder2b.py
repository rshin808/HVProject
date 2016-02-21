importg RPi.GPIO as gpio
import time



class Encoder2b:
    def __init__(self, PINS):
        self._ENCA = int(PINS["ENCA"])
        self._ENCB = int(PINS["ENCB"])
        self._ENCC = int(PINS["ENCC"])
        self._state = None

    def init_encoder(self, gpio):
        gpio.setup(self._ENCA, gpio.IN)
        gpio.setup(self._ENCB, gpio.IN)
        gpio.setup(self._ENCC, gpio.IN, pull_up_down = gpio.PUD_UP)
        self._state = self.__get_state(gpio)
        gpio.add_event_detect(self._ENCC, gpio.FALLING, bouncetime = 100)

    def __get_state(self, gpio):
        if gpio.input(self._ENCA) == True and gpio.input(self._ENCB) == True:
            return 3
        elif gpio.input(self._ENCA) == True and gpio.input(self._ENCB) == False:
            return 2
        elif gpio.input(self._ENCA) == False and gpio.input(self._ENCB) == True:
            return 1
        else:
            return 0

    def wait_hold(self, gpio):       
        if(gpio.event_detected(self._ENCC) == True):
            start = time.time()
            while(gpio.input(self._ENCC) == False):
                pass
            end = time.time()
            
            if float(end - start) >= 0.1 and float(end - start) < 0.5:
                return False
            elif float(end - start) >= 0.5:
                return True
            else:
                return None
        return None            

    def get_direction(self, gpio):
        new_state = self.__get_state(gpio)
        direction = "SAME"
        if new_state != self._state:
           if self._state == 1:
               if new_state == 3:
                   direction = "RIGHT"
               elif new_state == 0:
                   direction = "LEFT"
           elif self._state == 2:
               if new_state == 0:
                   direction = "RIGHT"
               elif new_state == 3:
                   direction = "LEFT"
           elif self._state == 3:
               if new_state == 2:
                   direction = "RIGHT"
               elif new_state == 1:
                   direction = "LEFT"
           else:
               if new_state == 1:
                   direction = "RIGHT"
               elif new_state == 2:
                   direction = "LEFT"
           self._state = new_state
           return direction
           
        else:
            return "SAME"

"""

gpio.setmode(gpio.BOARD)
PINS = {
    "ENCA" : 7, 
    "ENCB" : 21,
    "ENCC" : 16,
}
ENC = Encoder2b(PINS)
ENC.init_encoder(gpio)

try:
    while(True):
        ENC.wait(gpio)
except KeyboardInterrupt:
    gpio.cleanup()
except Exception, e:
    print e
    gpio.remove_event_detect(PINS["ENCC"])
    gpio.cleanup()
"""
