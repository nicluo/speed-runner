import Tkinter as tk
from ..lib.timer import Timer

from .redbutton import RedButton
from .numberdisplay import NumberDisplay

APP_WIDTH = 160
APP_HEIGHT = 60

class TimerWindow(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.timer = Timer()
        self.show_button = False
        self.up_button = None
        self.down_button = None
        self.number_display = None
        self.scale = 1.0
        self.render()

    def to_scale(self, n):
        return self.scale * n

    def running(self):
        return self.timer.running

    def expired(self):
        return self.timer.expired()

    def calculate_size(self):
        height = APP_HEIGHT
        width = APP_WIDTH
        if self.show_button:
            pass
        width = self.to_scale(width)
        height = self.to_scale(height)
        self.configure(width=width, height=height)
        return width, height

    def render(self):
        if self.number_display is not None:
            self.number_display.destroy()

        w, h = self.calculate_size()
        offset = 10
        if self.show_button:
            pass
        self.number_display = NumberDisplay(self, width=self.to_scale(160), height=self.to_scale(40))
        self.number_display.place(x=0, y=self.to_scale(offset), anchor="nw")

    def update_data(self):
        self.update_time()

    def update_time(self):
        self.number_display.set_time(self.timer.read())

    def on_trigger(self, event=None):
        self.timer.toggle()

    def on_reset(self):
        self.timer.reset()

    def on_hide_button(self):
        self.show_button = not self.show_button
        self.render()

    def on_resize_up(self):
        self.scale += 0.1
        self.render()

    def on_resize_down(self):
        self.scale -= 0.1
        self.scale = max(self.scale, 0.6)
        self.render()

    def on_increment(self):
        self.timer.increment(60)

    def on_decrement(self):
        self.timer.decrement(60)
