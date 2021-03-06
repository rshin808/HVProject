import csv
class Template_img:
    """
        This is the template for creating bitmaps.
        The template class only allows updte to the SEPS525.
        The bitmap is automatically updated using the oled commands.
    """
    def __init__(self, name, img):
        """
            This will create and initialize the template.
        """
        self._name = str(name)
        self._bitmap = []
        self._btest = []
        self.__create_bitmap(img)

    def __str__(self):
        return self._name

    def __create_bitmap(self, img):
        """
            This creates the bitmap for the template given an image.
            The bitmap values match the values for the SEPS525.
            Note: To reduce delay change .csv to have more than 2 values per row
        """
        with open(img, "rb") as img_csv:
            reader = csv.reader(img_csv)
            for row in reader:
                self._bitmap.append(tuple([int(row[0]), int(row[1])]))
    
    def update_oled(self, oled):
        oled.seps525_set_region(0, 0, 160, 128)
        oled.data_start()
        value = []
        for pixel in self._bitmap:
            value.append(pixel[0])
            value.append(pixel[1])
	
	for i in range(10):
            oled.data(value[(4096 * i): (4096 * i + 4096)])
        
    def name(self):
        return self._name

    def bitmap(self):
        return self._bitamp
"""
test = template_img("test", "VIMeas1.csv")
test.update_oled()
"""
