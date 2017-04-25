import os
import sys
import Tkinter as tk
import time
from PIL import Image, ImageTk, ImageFont, ImageDraw

BASE_DIR = sys._MEIPASS if getattr( sys, 'frozen', False ) else ''
FONT_PATH = 'assets/fonts/DSEG/fonts/DSEG7-Modern/DSEG7Modern-BoldItalic.ttf'

class NumberDisplay(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.font_size = 30
        self.canvas_image = None
        self.seconds = None
        self.set_time(0)

    def set_time(self, seconds):
        self.seconds = int(seconds)
        # Alternate colons every second
        if self.seconds % 2:
            format = '%H %M %S'
        else:
            format = '%H:%M:%S'
        time_string = time.strftime(format, time.gmtime(self.seconds))
        self.image = self._time_to_image(time_string)
        if self.canvas_image is not None:
            self.delete(self.canvas_image)
        self.canvas_image = self.create_image(82, 25, image=self.image)

    def _time_to_image(self, time_string):
        W, H = int(self['width']), int(self['height'])
        image = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(BASE_DIR, FONT_PATH),
                                  self.font_size)
        w, h = draw.textsize(time_string, font=font)
        draw.text(((W-w)/2,(H-h)/2), "88:88:88", font=font, fill=(240, 240, 240))
        draw.text(((W-w)/2,(H-h)/2), time_string, font=font, fill=(245, 29, 31))
        return ImageTk.PhotoImage(image)
