from text import Text_string as TS

B1LOFFSET = 10
B1TOPMARGIN = 0
B1ROWOFFSET = 16

B2LOFFSET = 10
B2TOPMARGIN = 0
B2ROWOFFSET = 16

def displayJustV(string):
    # This includes the "."
    return str(string).rjust(6)

def displayJustC(string):
    # This includes the "."
    return str(string).ljust(6, "0")

class Box1:
    """
        Class:  Box1
        Desc:   This is a box for displaying information. It includes a row for the title, voltage, and current. The box is active when a border appears.
                Selecting the box will result in another page being displayed.
    """
    def __init__(self, title = "", v = 0.0, c = 0.0, font = None, bg = (255, 255), textColor = (0, 0), xCoord = 0, yCoord = 0, nextPage = 0, currentPage = 0, channel = -1):
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
                    channel (int), the channel corresponding to the box
                        0: channel 1
                        1: channel 2
                        -1: no channel or N/A 
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
        self._channel = int(channel)
 
        self._active = False


        self._titleDisp = TS(self._x, self._y + B1TOPMARGIN, 14,self._title, self._font)
        self._vDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, displayJustV(v), self._font)
        self._cDisp = TS(self._x + B1LOFFSET, self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, displayJustC(c), self._font)
        self._vUnitDisp = TS(self._x + B1LOFFSET + len(self._vDisp), self._y + B1TOPMARGIN + B1ROWOFFSET, 14, " V", self._font)
        self._cUnitDisp = TS(self._x + B1LOFFSET + len(self._cDisp), self._y + B1TOPMARGIN + 2 * B1ROWOFFSET, 14, " mA", self._font)
        self._settings = []
        self._vSetDisp = None
        self._vSetUnitDisp = None

    def getSettings(self, settings = []):
        if self._channel != -1:
            self._settings = settings[self._channel]
            self._vSetDisp = TS(self._x + B1LOFFSET + len(self._vUnitDisp) + len(self._vDisp) + 20, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, displayJustV(self._settings[0]), self._font)        
            self._vSetUnitDisp = TS(self._x + B1LOFFSET + len(self._vSetDisp) + len(self._vUnitDisp) + len(self._vDisp) + 20, self._y + B1TOPMARGIN + B1ROWOFFSET, 14, " V", self._font)

    def updateSettings(self, settings = []):
        if self._channel != -1:
            settings[self._channel] = self._settings

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
        self._vUnitDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])
        self._cUnitDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])
        
        if self._channel != -1:
            self._vSetDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])
            self._vSetUnitDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])

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
        self._vDisp.update_string(displayJustV(self._v))
        self._cDisp.update_string(displayJustC(self._c))  
        self.drawBox(handlers)

class Box2:
    """
        Class:  Box2
        Desc:   This is the box for editting information.
                The box becomes active when self._active = True.
                The box allows editting when self._active = True and self._activeEdit = True.
                    When editting is allowed, 
                        pressing check will increment through self._editNumber 
                        holding check will set the self._editNumber
                        changing direction will change the self._editNumber[self._editIndex]

    """ 
    def __init__(self, title = "", v = 0.0, font1 = None, font2 = None, bg = (255, 255), textColor = (0, 0), xCoord = 0, yCoord = 0, nextPage = 0, currentPage = 0, channel = -1):
        """
            Name:   __init__
            Desc:   This initializes Box1.
            Params: title (string), the title of for the Box
                    v (float), the voltage field value of the Box
                    font1 (object), the font for the text
                    font2 (object), the font for the number
                    bg (tuple), the color of the background
                    textColor (tuple), the color for text
                    xCoord (int), the x position of the upper left corner of the Box
                    yCoord (int), the y position of the upper left corner of the Box
                    nextPage (int), the next page index number
                    currentPage (int), the current page index number
                    channel (int), the channel corresponding to the box
                        0: channel 1
                        1: channel 2
                        -1: no channel or N/A 
        """
        self._title = str(title)
        self._v = float(v)
        self._font1 = font1
        self._font2 = font2
        self._bg = bg
        self._textColor = textColor
        self._x = int(xCoord)
        self._y = int(yCoord)
        self._nextPage = int(nextPage)
        self._currentPage = int(currentPage)
        self._channel = int(channel)
        
        # active for highlighting box 
        self._active = False
        # activeEdit for editting box
        self._activeEdit = False
        # the index of the number
        self._editIndex = 0
        # edit number list
        self._editNumber = []
        
        self.updateEditNumber(0.0)

        self._titleDisp = TS(self._x, self._y + B2TOPMARGIN, 14,self._title, self._font1)
        self._vUnitDisp = TS(self._x + B2LOFFSET + 70, self._y + 20, 14, " V", self._font1)

        self._settings = []
        self._vSetDisp = None
        self._vSetUnitDisp = None

    def updateEditNumber(self, number = 0):
        l = 0
        j = 0
        for i in str(number).zfill(6):
            self._editNumber.append(TS(self._x + 20  + l, self._y + 20, 14, i, self._font2)) 
            
            l += len(self._editNumber[j])
            j += 1
       
    def drawEditNumber(self, handlers = []):
        handlers[0].draw_rect(self._x + 18, self._y + 18, 56, 18, (0, 0), False, handlers[1], handlers[2])
        for i in range(6):
            self._editNumber[i].draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2]) 

    def getSettings(self, settings = []):
        if self._channel != -1:
            # get the settings on page initialization
            self._settings = settings[self._channel]
            settingString = str(self._settings).zfill(6)

    def updateSettings(self, settings = []):
        if self._channel != -1:
            settings[self._channel] = self._settings

    def setActive(self, active = False):
        self._active = active

    def drawBox(self, handlers = []):
        if self._active == True:
            handlers[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (0, 0), False, handlers[1], handlers[2]) 
        else:
            handlers[0].draw_rect((self._x - 2), (self._y - 2), 144, 48, (255, 255), False, handlers[1], handlers[2]) 
        self._titleDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2]) 
        self.drawEditNumber(handlers)
        self._vUnitDisp.draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])
        

    def updateCheck(self, check = None, handlers = []):
        """
            Name:   updateCheck
            Desc:   This is run everything the check button is called on the box.
                    if editting is active:
                        if check is held:
                            the editNumber is set
                        if check is pressed:
                            the editIndex in incremented
                    else:
                        if check is pressed:
                            editting is activated

            Params: check (bool), the check if the button is pressed, held, or NA
                    handlers (list), the list of handlers for the box
        """
        if check != None:
            if check == True:
                # check held
                # this only locks in the number if activeEdit is True 
                # this will also draw the appropriate display
                if self._activeEdit == True:
                    self._activeEdit = False
                    self.drawEditNumber(handlers)
                    self._editIndex = 0
                    
                    # save the settings
                    numbers = ""
                    
                    for number in self._editNumber:
                        numbers += str(number)

                    numbers = round(float(numbers), 1)
                    self._settings[0] = numbers
            else:
                # check Pressed
                # this affects multiple states dependent on active and activeEdit
                # if active is True, then activeEdit becomes True (activeEdit being True means active is also True)
                # if activeEdit is True, then number index is incremented
                # this will also draw the appropriate display
                if self._activeEdit == True:
                   self._editNumber[self._editIndex].draw_string(self._textColor, self._bg, handlers[0], spi = handlers[1], gpio = handlers[2])
                   self._editIndex += 1

                   if self._editIndex == 4:
                       self._editIndex += 1
                   if self._editIndex == 6:
                       self._editIndex = 0

                   self._editNumber[self._editIndex].draw_string(self._bg, self._textColor, handlers[0], spi = handlers[1], gpio = handlers[2])
                    
                else:
                   self._activeEdit = True
                   self._editIndex = 0
                   self._editNumber[self._editIndex].draw_string(self._bg, self._textColor, handlers[0], spi = handlers[1], gpio = handlers[2])
            
            # this box does not change pages
            return self._currentPage 
        else:
            # this box does not change pages
            return self._currentPage

    def updateDirection(self, direction = None, selections = 0, index = 0, handlers = []):
        """
            Name:   updateDirection
            Desc:   This updates the direction of the box.
                    If editting is active:
                        left decreases the current editNumber value by 1
                        right increases the current editNumber value by 1

                        note: the values allowed are 0 <= editNumber <= 9.
                    If editting is not active:
                        left returns the box index previous
                        right returns the next box index

            Params: direction (bool), the direction either left, right, or NA
                    selections (int), this is the maximum number of boxes available on the page
                    index (int), the current index
                    handlers (list), the handlers for the box
        """
        if self._activeEdit == False:
            # Chooses the next box if not active
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
        else:
            # Update the numbers in the currently selected box
            if direction == -1:
                 number = int(str(self._editNumber[self._editIndex]))
                 number -= 1
                 if number <= 0:
                     number = 0

                 self._editNumber[self._editIndex].update_string(str(number))
                 self._editNumber[self._editIndex].draw_string(self._bg, self._textColor, handlers[0], spi = handlers[1], gpio = handlers[2])

            elif direction == 1:
                 number = int(str(self._editNumber[self._editIndex]))
                 number += 1
                 if number >= 9:
                     number = 9
                     
                 self._editNumber[self._editIndex].update_string(str(number))
                 self._editNumber[self._editIndex].draw_string(self._bg, self._textColor, handlers[0], spi = handlers[1], gpio = handlers[2])  

            # Return the index of this box
            return index
         

    def timedUpdate(self, params = [], handlers = []):
        pass
