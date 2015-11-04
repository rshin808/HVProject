import PINS
import Adafruit_BBIO.GPIO as GPIO

class BBB:
    def __init__(self, PINS = None, GPIO):
        self._PINS = PINS
        self._init(PINS, GPIO)

    def _init(self, PINS, GPIO):
        GPIO.setup(PINS["ADC_A/B"], )
        GPIO.setup(PINS["RE_SWTICH"], )
        GPIO.setup(PINS["RE_A"], )
        GPIO.setup(PINS["RE_B"], )
        GPIO.setup(PINS["HVO/F_4"], )
        GPIO.setup(PINS["EN1"], )
        GPIO.setup(PINS["EN2"], )
        GPIO.setup(PINS["EN3"], )
        GPIO.setup(PINS["EN4"], )
        GPIO.setup(PINS["ADC_CONV"], )
        GPIO.setup(PINS["HVO/F_1"], )

    def adcConv(self, GPIO = None, OF = None):
        GPIO.

