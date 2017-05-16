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
        self.show_button = True

    def render(self):
        pass

    def running(self):
        return False

    def update_data(self):
        pass
