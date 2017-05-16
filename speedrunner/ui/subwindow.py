"""
Tkinter-based UI
"""

import time
import Tkinter as tk
from ..lib.mode import Mode

from .borderedframe import BorderedFrame
from .stopwatchwindow import StopWatchWindow
from .timerwindow import TimerWindow

WINDOW_PADDING = 50

class SubWindow(tk.Toplevel):
    """Sticky, always-on-top window for the main UI"""
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.mode = Mode.STOPWATCH
        self.stop_watch_window = None
        self.timer_window = None
        self.active_window = None
        self.frame = None
        self.window_config()
        self.render()
        self.update_data()

    def resize_frame(self):
        self.active_window.update_idletasks()
        w = self.active_window.winfo_width()
        h = self.active_window.winfo_height()
        self.frame.dimensions(w, h)

    def render(self):
        if self.frame is not None:
            self.frame.destroy()
        if self.active_window is not None:
            self.active_window.destroy()
            self.active_window = None
        self.frame = BorderedFrame(self)
        self.frame.pack()
        if self.mode == Mode.STOPWATCH:
            self.stop_watch_window = StopWatchWindow(self.frame.inner_canvas)
            self.stop_watch_window.place(bordermode='inside', x=0, y=0, anchor='nw')
            self.active_window = self.stop_watch_window
        elif self.mode == Mode.TIMER:
            self.timer_window = TimerWindow(self.frame.inner_canvas)
            self.timer_window.place(bordermode='inside', x=0, y=0, anchor='nw')
            self.active_window = self.timer_window
        self.resize_frame()
        self.fix_to_top_right()

    def window_config(self):
        self.overrideredirect(1)
        self.lift()
        self.wm_attributes('-topmost', 1)

    def fix_to_top_right(self):
        screen_width = self.winfo_screenwidth()
        left = '+' + str(screen_width - WINDOW_PADDING - int(self.active_window.winfo_width()))
        top = '+' + str(WINDOW_PADDING)
        self.geometry(left + top)

    def update_data(self):
        if self.active_window is not None:
            self.active_window.update_data()
        self.update_border()
        self.after(100, self.update_data)

    def update_border(self):
        if self.active_window:
            if self.active_window.running():
                if self.active_window.expired():
                    self.update_border_expired()
                else:
                    self.frame.border('red')
        else:
            self.frame.border('black')

    def update_border_expired(self):
        if int(time.time() * 2) % 2:
            self.frame.border('red')
        else:
            self.frame.border('black')

    def dispatch_event(self, event):
        def call(e):
            dispatch_name = 'on_' + event
            try:
                dispatch_next = getattr(self.active_window, dispatch_name)
            except AttributeError:
                pass
            else:
                dispatch_next()
            try:
                dispatch_self = getattr(self, dispatch_name)
            except AttributeError:
                pass
            else:
                dispatch_self()
        return call

    def on_resize_up(self):
        self.resize_frame()
        self.fix_to_top_right()

    def on_resize_down(self):
        self.resize_frame()
        self.fix_to_top_right()

    def on_hide_button(self):
        self.resize_frame()

    def on_split_next(self):
        self.resize_frame()

    def on_split_previous(self):
        self.resize_frame()

    def on_mode_toggle(self):
        if not self.active_window.running():
            if self.mode == Mode.STOPWATCH:
                self.mode = Mode.TIMER
            elif self.mode == Mode.TIMER:
                self.mode = Mode.STOPWATCH
            self.render()
