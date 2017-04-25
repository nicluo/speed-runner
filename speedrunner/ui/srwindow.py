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

APP_WIDTH = 180
APP_HEIGHT = 180
WINDOW_PADDING = 50

class SRWindow(tk.Tk):
    """Root window for Tkinter.

    This hidden window is required to bind keyboard keys
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.s = SubWindow(self)
        self.hide()
        self.bind_keys()

    def bind_keys(self):
        # Stopwatch keybindings
        self.bind_all("<space>", self.s.on_trigger)
        self.bind_all("<r>", self.s.on_reset)
        self.bind_all("<n>", self.s.split_next)
        self.bind_all("<p>", self.s.split_previous)
        # Timer
        # self.bind_all("<m>", self.s.on_mode_change)
        # self.bind_all("<up>", self.s.on_increment)
        # self.bind_all("<down>", self.s.on_decrement)
        # Window/ Appearance keybindings
        # self.bind_all("<m>", self.s.on_mode_toggle)
        # self.bind_all("<l>", self.s.on_lock_toggle)
        self.bind_all("<h>", self.s.on_hide_button)
        self.bind_all("<plus>", self.s.on_resize_up)
        self.bind_all("<minus>", self.s.on_resize_down)

    def hide(self):
        """
        Setting height and width to 0 makes the window invisible
        but lets keypresses register.
        """
        self.geometry("%dx%d%+d%+d" % (0, 0, 0, 0))

class SubWindow(tk.Toplevel):
    """Sticky, always-on-top window for the main UI"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.window_config()
        self.fix_to_top_right()
        self.pack_frame()
        self.place_red_button()
        self.number_display = NumberDisplay(self.frame, width=160, height=40)
        self.place_number_display()
        self.stop_watch = StopWatch()
        self.timer = Timer()
        self.show_button = False
        self.split_number_displays = []
        self.update()

    def render(self):
        if self.show_button:
            pass

    def update(self):
        self.number_display.set_time(self.stop_watch.read())
        self.after(100, self.update)

    def pack_frame(self):
        self.frame = BorderedFrame(self, width=APP_WIDTH, height=APP_HEIGHT)
        self.frame.pack()

    def place_red_button(self):
        self.redButton = RedButton(self.frame)
        self.redButton.bind("<<Click>>", self.on_trigger)
        self.redButton.place(bordermode='inside', x=(APP_WIDTH-100)/2,  y=15)

    def remove_red_button(self):
        self.redButton.destroy()

    def place_number_display(self):
        self.number_display.place(bordermode='inside', x=(APP_WIDTH-160)/2,  y=125)

    def window_config(self):
        self.overrideredirect(1)
        self.lift()
        self.wm_attributes('-topmost', 1)

    def fix_to_top_right(self):
        screen_width = self.winfo_screenwidth()
        left = '+' + str(screen_width - WINDOW_PADDING - APP_WIDTH)
        top = '+' + str(WINDOW_PADDING)
        self.geometry(left + top)

    def on_trigger(self, event):
        self.stop_watch.toggle()
        if(self.stop_watch.running):
            self.frame.border('red')
        else:
            self.frame.border('black')

    def on_resize_up(self, event):
        pass

    def on_resize_down(self, event):
        pass

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
