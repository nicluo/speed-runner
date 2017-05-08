"""
Tkinter-based UI
"""

import sys
import Tkinter as tk
from ..lib.stopwatch import StopWatch
from ..lib.timer import Timer

from .redbutton import RedButton
from .numberdisplay import NumberDisplay
from .borderedframe import BorderedFrame

APP_WIDTH = 160
APP_HEIGHT = 170
WINDOW_PADDING = 50

class Mode:
    STOPWATCH = 1
    TIMER = 2

class SubWindow(tk.Toplevel):
    """Sticky, always-on-top window for the main UI"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.stop_watch = StopWatch()
        self.timer = Timer()
        self.mode = Mode.STOPWATCH
        self.show_button = True
        self.split_number_displays = []
        self.scale = 1
        self.frame = None
        self.window_config()
        self.render()
        self.update()

    def calculate_size(self):
        self.height = APP_HEIGHT * self.scale
        self.width = APP_WIDTH * self.scale
        if len(self.stop_watch.splits) > 1:
            self.height += (len(self.stop_watch.splits) * 30 * self.scale)
        if not self.show_button:
            self.height -= 110 * self.scale

    def render(self):
        self.calculate_size()
        offset = 10 * self.scale
        if self.frame is not None:
            self.frame.destroy()
        self.frame = BorderedFrame(self, width=self.width, height=self.height)
        if(self.stop_watch.running):
            self.frame.border('red')
        self.frame.pack()
        if self.show_button:
            self.redButton = RedButton(self.frame.inner_canvas, width=100*self.scale, height=100*self.scale)
            self.redButton.bind("<<Click>>", self.on_trigger)
            self.redButton.place(bordermode='inside', x=(self.width-int(self.redButton['width']))/2,  y=offset)
            offset += 110 * self.scale
        self.number_display = NumberDisplay(self.frame.inner_canvas, width=160*self.scale, height=40*self.scale)
        self.number_display.place(bordermode='inside', x=0, y=offset, anchor="nw")
        self.split_number_displays = []
        if len(self.stop_watch.splits) > 1:
            for i in xrange(len(self.stop_watch.splits)):
                split_display = NumberDisplay(self.frame.inner_canvas, width=120*self.scale, height=30*self.scale)
                split_display.place(bordermode='inside', x=40*self.scale, y=offset + (i*30 + 50)*self.scale, anchor="nw")
                self.split_number_displays.append(split_display)
        self.fix_to_top_right()

    def update(self):
        self.number_display.set_time(self.stop_watch.read())
        for i in xrange(len(self.split_number_displays)):
            self.split_number_displays[i].set_time(self.stop_watch.splits[i].seconds())
        self.after(100, self.update)

    def remove_red_button(self):
        self.redButton.destroy()

    def window_config(self):
        self.overrideredirect(1)
        self.lift()
        self.wm_attributes('-topmost', 1)

    def fix_to_top_right(self):
        screen_width = self.winfo_screenwidth()
        left = '+' + str(screen_width - WINDOW_PADDING - int(self.width))
        top = '+' + str(WINDOW_PADDING)
        self.geometry(left + top)

    def on_trigger(self, event):
        self.stop_watch.toggle()
        if(self.stop_watch.running):
            self.frame.border('red')
        else:
            self.frame.border('black')

    def on_resize_up(self, event):
        self.scale += 0.1
        self.render()

    def on_resize_down(self, event):
        self.scale -= 0.1
        self.scale = max(self.scale, 0.6)
        self.render()

    def on_reset(self, event):
        self.stop_watch.reset()
        self.render()

    def on_hide_button(self, event):
        self.show_button = not self.show_button
        self.render()

    def split_next(self, event):
        self.stop_watch.split_next()
        self.render()

    def split_previous(self, event):
        self.stop_watch.split_previous()
        self.render()
