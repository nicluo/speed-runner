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
            "<r>": self.s.dispatch_event('reset'),
            "<h>": self.s.dispatch_event('hide_button'),
            "<plus>": self.s.dispatch_event('resize_up'),
            "<minus>": self.s.dispatch_event('resize_down'),
            "<space>": self.s.dispatch_event('trigger'),
            "<m>": self.s.dispatch_event('mode_toggle'),
        }

        self.timer_hotkeys = {
            "<Up>": self.s.dispatch_event('increment'),
            "<Down>": self.s.dispatch_event('decrement'),
        }

        self.stopwatch_hotkeys = {
            "<n>": self.s.dispatch_event('split_next'),
            "<p>": self.s.dispatch_event('split_previous'),
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
