from text import Text_string as TS

B1LOFFSET = 10
B1TOPMARGIN = 0
B1ROWOFFSET = 16

def displayJust(string):
    # This includes the "."
    return str(string).rjust(6)

class Box1:
    def __init__(self, title = "", v = 0, c = 0, font = None, bg = (255, 255), textColor = (0, 0), xCoord = 0, yCoord = 0, nextPage = 0, currentPage = 0):
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
                    currentPage (int), the current page index number
        """
        self._title = str(title)
        self._v = float(v)
        self._c = float(c)
        self._font = font
        self._bg = bg
        self._textColor = textColor
        self._x = int(xCoord)
        self._y = int(yCoord)
        self._nextPage = int(nextPage)
        self._currentPage = int(currentPage) 
        self._active = False


        self._titleDisp = TS(self._x, self._y + B1TOPMARGIN, 14,self._title, self._font)
        self._vDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, displayJust(v), self._font)
        self._cDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, displayJust(c), self._font)
        self._vUnitDisp = TS(len(self._vDisp), self._y + B1TOPMARGIN + B1ROWOFFSET, 14, " [V]", self._font)
        self._cUnitDisp = TS(len(self._cDisp), self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, " [mA]", self._font)

    def setActive(self, active = False):
        self._active = active

    def drawBox(self, handlers = []):
        if self._active == True:
            handlers[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (0, 0), False, handlers[1], handlers[2]) 
        else:
            handlers[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (255, 255), False, handlers[1], handlers[2]) 
        self._titleDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2]) 
        self._vDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2]) 
        self._cDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2]) 

    def updateCheck(self, check = None, handlers = []):
        if check != None:
            return self._nextPage 
        else:
            return self._currentPage

    def updateDirection(self, direction = None, selections = 0, index = 0, handlers = []):
        currentActive = index
        if direction == -1:
            currentActive -= 1
            if currentActive < 0:
                currentActive = 0
            self._active = False

        elif direction == 1:
            currentActive += 1
            if currentActive >= selections:
                currentActive = selections - 1
            self._active = False
        self.drawBox(handlers)
        return currentActive
         

    def timedUpdate(self, params = [], handlers = []):
        self._v = params[0]
        self._c = params[1]
        self._vDisp.update_string(displayJust(self._v))
        self._cDisp.update_string(displayJust(self._c))  
        self.drawBox(handlers)
