from text import Text_string as TS

# handlers = [display, spi, gpio]
# params = [[CH1V, CH1C], [CH2V, CH2C]]

class Page:
    def __init__(self, title = "", boxes = [], pageNumber = 0):
        self._title = str(title)
        self._boxes = boxes
        self._pageNumber = int(pageNumber)
        self._activeBox = 0

    def __iter__(self):
        for box in self._boxes:
            yield box

    def drawPage(self, font = None, handlers = []):
        handlers[0].fill_screen((255, 255), handlers[1], handlers[2])
        for i in range(len(self._boxes)):
            if i == self._activeBox:
                self._boxes[i].setActive(True)
            else:
                self._boxes[i].setActive(False)
            self._boxes[i].drawBox(handlers)
        TS(10, 10, 14, self._title, font).draw_string((0, 0), (255, 255), handlers[0], handlers[2], handlers[1])
        

    def updateCheck(self, check = None, handlers = []):
        return self._boxes[self._activeBox].updateCheck(check, handlers)        

    def updateDirection(self, direction = None, handlers = []):
        self._activeBox = self._boxes[self._activeBox].updateDirection(direction, len(self._boxes), self._pageNumber, handlers)
        self._boxes[self._activeBox].setActive(True)
        self._boxes[self._activeBox].drawBox(handlers)
        
    def timedUpdate(self, params = [], handlers = []):
        # params must be in order of the boxes
        for i in range(len(params)):
            self._boxes[i].timedUpdate(params[i], handlers)
        
        

