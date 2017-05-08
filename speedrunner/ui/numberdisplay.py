import os
import sys
import Tkinter as tk
import time
from PIL import Image, ImageTk, ImageFont, ImageDraw

BASE_DIR = sys._MEIPASS if getattr( sys, 'frozen', False ) else ''
FONT_PATH = 'assets/fonts/DSEG/fonts/DSEG7-Modern/DSEG7Modern-BoldItalic.ttf'
FOREGROUND_COLOUR = (245, 29, 31)
BACKGROUND_COLOUR = (240, 240, 240)
Y_OFFSET = 1
X_OFFSET = 3

class NumberDisplay(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.width = int(self['width'])
        self.height = int(self['height'])
        self.canvas_image = None
        self.seconds = None
        self.font_path = os.path.join(BASE_DIR, FONT_PATH)
        self._calc_font_size()
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
        self.canvas_image = self.create_image(X_OFFSET, Y_OFFSET, image=self.image, anchor="nw")

    def _calc_font_size(self):
        W, H = self.width, self.height
        font_size = self.height
        image = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(image)
        while True:
            font = ImageFont.truetype(self.font_path, font_size)
            w, h = draw.textsize("88:88:88", font=font)
            if w <= W and h <= H:
                break;
            font_size -= 1
        self.font_size = font_size

    def _time_to_image(self, time_string):
        W, H = self.width, self.height
        image = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, self.font_size)
        w, h = draw.textsize(time_string, font=font)
        draw.text(((W-w)/2,(H-h)/2), "88:88:88", font=font, fill=BACKGROUND_COLOUR)
        draw.text(((W-w)/2,(H-h)/2), time_string, font=font, fill=FOREGROUND_COLOUR)
        return ImageTk.PhotoImage(image)
