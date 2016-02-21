from text import Text_string as TS

class Page:
    def __init__(self, title = "", box1 = None, box2 = None, box3 = None, pages = []):
        self._title = str(title)
        self._box1 = box1
        self._box2 = box2
        self._box3 = box3
        self._active = 0
        self._pages = pages

    def getBox(self, box = 1):
        if box == 1:
            return self._box1.getBox()
        elif box == 2:
            return self._box2.getBox() 
        elif box == 3:
            return self._box3.getBox()

    def updateBox(self, box = 1, params = []):
        if box == 1:
            self._box1.updateBox(params)
        elif box == 2:
            self._box2.updateBox(params)
        elif box == 3:
            self._box3.updateBox(params)

    def drawBox(self, box = 1, params = []):
        if box == 1:
            self._box1.drawBox(params)
        elif box == 2:
            self._box2.drawBox(params)
        elif box == 3:
            self._box3.drawBox(params)
   
    def setActive(self, direction):
        if direction == -1:
            if self._active > 0:
                self._active -= 1
        elif direction == 1:
            if self._active < 3:
                if self._box3 != None:
                    self._active += 1
                else:
                    self._active = 2

    def setBoxActive(self, params = []):
        if self._active == 0:
            self._box1.setActive(True, params)      
            self._box2.setActive(False, params)       
            if self._box3 != None:
                self._box3.setActive(False, params)

        elif self._active == 1:
            self._box1.setActive(False, params)
            self._box2.setActive(True, params)
            if self._box3 != None:
                self._box3.setActive(False, params)

        elif self._active == 2:
            self._box1.setActive(False, params)
            self._box2.setActive(False, params)
            if self._box3 != None:
                self._box3.setActive(True, params)            

    def drawPage(self, display = None, spi = None, gpio = None, font = None):
        display.fill_screen((255, 255), spi, gpio)
        self.setBoxActive()
        TS(10, 10, 14, self._title, font).draw_string((0, 0), (255, 255), display, gpio, spi)
        self.drawBox(1, [display, spi, gpio]) 
        self.drawBox(2, [display, spi, gpio]) 
        if self._box3 != None:
            self.drawBox(3, [display, spi, gpio])


    def updateDirection(self, direction = None, params = []):
        self.setActive(direction)
        self.setBoxActive(params)

    def updateCheck(self, check = None, params = []):
        if self._active == 0:
            return self._box1.updateCheck(check, params)
        elif self._active == 1:
            return self._box2.updateCheck(check, params)
        elif self._active == 2:
            return self._box3.updateCheck(check, params)
