"""
Tkinter-based UI
"""

import sys
import Tkinter as tk

from .redbutton import RedButton
from .numberdisplay import NumberDisplay
from .borderedframe import BorderedFrame
from .subwindow import SubWindow

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

        self.hotkeys = {
            "<r>": self.s.on_reset,
            "<h>": self.s.on_hide_button,
            "<plus>": self.s.on_resize_up,
            "<minus>": self.s.on_resize_down,
            "<space>": self.s.on_trigger,
            # "<m>": self.s.on_mode_toggle,
        }

        self.timer_hotkeys = {
            # "<up>": self.s.increment,
            # "<down>": self.s.decrement,
        }

        self.stopwatch_hotkeys = {
            "<n>": self.s.split_next,
            "<p>": self.s.split_previous,
        }

        self.hotkeys.update(self.timer_hotkeys)
        self.hotkeys.update(self.stopwatch_hotkeys)
        self.bind_keys()

    def bind_keys(self):
        for key in self.hotkeys:
            self.bind_all(key, self.hotkeys[key])

    def hide(self):
        """
        Setting height and width to 0 makes the window invisible
        but lets keypresses register.
        """
        self.geometry("%dx%d%+d%+d" % (0, 0, 0, 0))
