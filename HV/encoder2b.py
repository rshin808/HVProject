import RPi.GPIO as gpio
import time



class Encoder2b:
    def __init__(self, PINS):
        self._ENCA = int(PINS["ENCA"])
        self._ENCB = int(PINS["ENCB"])
        self._ENCC1 = int(PINS["ENCC1"])
        self._ENCC2 = int(PINS["ENCC2"])
        self._state = None

    def init_encoder(self, gpio):
        gpio.setup(self._ENCA, gpio.IN)
        gpio.setup(self._ENCB, gpio.IN)
        gpio.setup(self._ENCC2, gpio.IN)
        gpio.setup(self._ENCC1, gpio.IN, pull_up_down = gpio.PUD_UP)
        self._state = self.__get_state(gpio)
        gpio.add_event_detect(self._ENCC1, gpio.FALLING, bouncetime = 300)

    def __get_state(self, gpio):
        if gpio.input(self._ENCA) == True and gpio.input(self._ENCB) == True:
            return 3
        elif gpio.input(self._ENCA) == True and gpio.input(self._ENCB) == False:
            return 2
        elif gpio.input(self._ENCA) == False and gpio.input(self._ENCB) == True:
            return 1
        else:
            return 0

    def wait(self, gpio):
        if(gpio.event_detected(self._ENCC1) == True):
            start = time.time()
    
    def __pressed(self, gpio, start):
        print "called"
        end = time.time()
        while(gpio.input(self._ENCC2) == False):
            end = time.time()
            print "here"
        print str(end - start)

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
            return "Same"

gpio.setmode(gpio.BOARD)
PINS = {
    "ENCA" : 7, 
    "ENCB" : 21,
    "ENCC1" : 16,
    "ENCC2" : 24,
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
    gpio.remove_event_detect(PINS["ENCC1"])
    gpio.cleanup()
