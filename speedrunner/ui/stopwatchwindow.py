import Tkinter as tk
from ..lib.stopwatch import StopWatch

from .redbutton import RedButton
from .numberdisplay import NumberDisplay

APP_WIDTH = 160
APP_HEIGHT = 60

class StopWatchWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.stop_watch = StopWatch()
        self.show_button = True
        self.red_button = None
        self.number_display = None
        self.split_number_displays = []
        self.scale = 1.0
        self.render()

    def running(self):
        return self.stop_watch.running

    def expired(self):
        return False

    def to_scale(self, n):
        return self.scale * n

    def calculate_size(self):
        height = APP_HEIGHT
        width = APP_WIDTH
        if self.show_button:
            height += 110
        if len(self.stop_watch.splits) > 1:
            height += len(self.stop_watch.splits) * 30
        width = self.to_scale(width)
        height = self.to_scale(height)
        self.configure(width=width, height=height)
        return width, height

    def render(self):
        if self.red_button is not None:
            self.red_button.destroy()
        if self.number_display is not None:
            self.number_display.destroy()
        for split in self.split_number_displays:
            split.destroy()

        w, h = self.calculate_size()
        offset = 10
        if self.show_button:
            self.red_button = RedButton(self, width=self.to_scale(100), height=self.to_scale(100))
            self.red_button.bind("<<Click>>", self.on_trigger)
            self.red_button.place(x=(w-int(self.red_button['width']))/2,  y=self.to_scale(offset))
            offset += 110
        self.number_display = NumberDisplay(self, width=self.to_scale(160), height=self.to_scale(40))
        self.number_display.place(x=0, y=self.to_scale(offset), anchor="nw")
        self.split_number_displays = []
        if len(self.stop_watch.splits) > 1:
            for i in xrange(len(self.stop_watch.splits)):
                split_display = NumberDisplay(self, width=self.to_scale(120), height=self.to_scale(30))
                split_display.place(bordermode='inside', x=self.to_scale(40), y=self.to_scale(offset + (i*30 + 50)), anchor="nw")
                self.split_number_displays.append(split_display)

    def update_data(self):
        self.update_time()
        self.update_splits()

    def update_time(self):
        self.number_display.set_time(self.stop_watch.read())

    def update_splits(self):
        for i in xrange(len(self.split_number_displays)):
            self.split_number_displays[i].set_time(self.stop_watch.splits[i].seconds())

    def on_trigger(self, event=None):
        self.stop_watch.toggle()

    def on_reset(self):
        self.stop_watch.reset()

    def on_hide_button(self):
        self.show_button = not self.show_button
        self.render()

    def on_split_next(self):
        self.stop_watch.split_next()
        self.render()

    def on_split_previous(self):
        self.stop_watch.split_previous()
        self.render()

    def on_resize_up(self):
        self.scale += 0.1
        self.render()

    def on_resize_down(self):
        self.scale -= 0.1
        self.scale = max(self.scale, 0.6)
        self.render()
