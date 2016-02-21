from text import Text_string as TS

B1LOFFSET = 10
B1TOPMARGIN = 0
B1ROWOFFSET = 16

def displayJust(string):
    return str(string).rjust(6)

class Box1:
    def __init__(self, title = "", v = 0, c = 0, font = None, bg = (255, 255), textColor = (0, 0), xCoord = 0, yCoord = 0, nextPage = 0):
        """
            Name:   __init__
            Desc:   This initializes Box1.
            Params: title (string), the title of for the Box
                    v (float), the voltage field value of the Box
                    c (float), the current field value of the Box
                    font (object), the font for the text
                    bg (tuple), the color of the background
                    textColor (tuple), the color for text
                    xCoord (int), the x position of the upper left corner of the Box
                    yCoord (int), the y position of the upper left corner of the Box
                    nextPage (int), the next page index number
        """
        self._title = str(title)
        self._v = v
        self._c = c
        self._font = font
        self._bg = bg
        self._textColor = textColor
        self._x = xCoord
        self._y = yCoord
        self._titleDisp = TS(self._x, self._y + B1TOPMARGIN, 14,self._title, self._font)
        self._vDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, displayJust(v), self._font)
        self._cDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, displayJust(c), self._font)
        self._vUnitDisp = TS(len(self._vDisp), self._y + B1TOPMARGIN + B1ROWOFFSET, 14, " [V]", self._font)
        self._cUnitDisp = TS(len(self._cDisp), self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, " [mA]", self._font)
        self._active = False
        self._nextPage = nextPage

    def getBox(self):
        return True
         
    def updateBox(self, params):
        """
            Name:   updateBox
            Desc:   This updates the box information.
            Params: params (list), contains the update information.
                        params[0]:  XCoordinate
                        params[1]:  YCoordinate
                        params[2]:  Background Color
                        params[3]:  Text Color
                        params[4]:  Voltage in [V]
                        params[5]:  Current in [mA]
                    Note:   The X and Y Coordinates should be the upper left corner of the Box.
                            Also changing the X and Y Coordinates require hiding the original text string.
        """
        if params[0] != None:
            self._x = params[0]
            self._titleDisp.x = self._x
            self._vDisp.x = self._x + B1LOFFSET
            self._cDisp.x = self._x + B1LOFFSET

        if params[1] != None:
            self._y = params[1]
            self._titleDisp.y = self._y + B1TOPMARGIN
            self._vDisp.y = self._y + B1TOPMARGIN + B1ROWOFFSET
            self._cDisp.y = self._y + B1TOPMARGIN + 2 * B1ROWOFFSET

        if params[2] != None:
            self._bg = params[2]

        if params[3] != None:
            self._textColor = params[3]
            
        if params[4] != None:
            self._v = params[4]
            self._vDisp.update_string(displayJust(self._v))

        if params[5] != None:
            self._c = params[5]
            self._cDisp.update_string(displayJust(self._c))


    def drawBox(self, params):
        """
            Name:   drawBox
            Desc:   This draws the Box.
            Params: params (list), contains the handlers.
                        params[0]:  Display
                        params[1]:  SPI
                        params[2]:  GPIO
        """
        if self._active == True:
            params[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (0, 0), False, params[1], params[2]) 
        else:
            params[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (255, 255), False, params[1], params[2]) 
        self._titleDisp.draw_string(self._textColor, self._bg, params[0], spi = params[1], gpio = params[2]) 
        self._vDisp.draw_string(self._textColor, self._bg, params[0], spi = params[1], gpio = params[2]) 
        self._cDisp.draw_string(self._textColor, self._bg, params[0], spi = params[1], gpio = params[2]) 
    
    def getActive(self):
        return self._active

    def setActive(self, enable = True, params = []):
        self._active = enable

    def updateCheck(self, check, params):
        if check == True:
            # Held
            #print self._title + " Held"
            return self._nextPage
        elif check == False:
            # Pressed
            #print self._title + " Pressed"
            return self._nextPage
class Box2:
    def __init__(self, title = "", v = 0, font = None, bg = (255, 255), textColor = (0, 0), xCoord = 0, yCoord = 0, nextPage = 0):
        """
            Name:   __init__
            Desc:   This initializes Box2. Box2 contains a field for maniuplating a number as well as a Cancel or Accept.
            Params: title (string), the title of for the Box
                    v (float), the voltage field value of the Box
                    font (object), the font for the text
                    bg (tuple), the color of the background
                    textColor (tuple), the color for text
                    xCoord (int), the x position of the upper left corner of the Box
                    yCoord (int), the y position of the upper left corner of the Box
                    nextPage (int), the next page index
        """
        self._title = str(title)
        self._v = v
        self._font = font
        self._bg = bg
        self._textColor = textColor
        self._x = xCoord
        self._y = yCoord
        self._titleDisp = TS(self._x, self._y + B1TOPMARGIN, 14,self._title, self._font)
        self._vDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, displayJust(v), self._font)
        self._vUnitDisp = TS(len(self._vDisp), self._y + B1TOPMARGIN + B1ROWOFFSET, 14, " [V]", self._font)
        self._active = False
        self._nextPage = nextPage
    
    def getBox(self):
        return False 
         
    def updateBox(self, params):
        """
            Name:   updateBox
            Desc:   This updates the box information.
            Params: params (list), contains the update information.
                        params[0]:  XCoordinate
                        params[1]:  YCoordinate
                        params[2]:  Background Color
                        params[3]:  Text Color
                        params[4]:  Voltage in [V]
                    Note:   The X and Y Coordinates should be the upper left corner of the Box.
                            Also changing the X and Y Coordinates require hiding the original text string.
        """
        if params[0] != None:
            self._x = params[0]
            self._titleDisp.x = self._x
            self._vDisp.x = self._x + B1LOFFSET

        if params[1] != None:
            self._y = params[1]
            self._titleDisp.y = self._y + B1TOPMARGIN
            self._vDisp.y = self._y + B1TOPMARGIN + B1ROWOFFSET

        if params[2] != None:
            self._bg = params[2]

        if params[3] != None:
            self._textColor = params[3]
            
        if params[4] != None:
            self._v = params[4]
            self._vDisp.update_string(displayJust(self._v))

    def drawBox(self, params):
        """
            Name:   drawBox
            Desc:   This draws the Box.
            Params: params (list), contains the handlers.
                        params[0]:  Display
                        params[1]:  SPI
                        params[2]:  GPIO
        """
        if self._active == True:
            params[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (0, 0), False, params[1], params[2]) 
        else:
            params[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (255, 255), False, params[1], params[2]) 
        self._titleDisp.draw_string(self._textColor, self._bg, params[0], spi = params[1], gpio = params[2]) 
        self._vDisp.draw_string(self._textColor, self._bg, params[0], spi = params[1], gpio = params[2]) 
    
    def getActive(self):
        return self._active

    def setActive(self, enable = True, params = []):
        self._active = enable

    def updateCheck(self, check, params):
        if check == True:
            # Held
            pass
        elif check == False:
            # Pressed
            pass
