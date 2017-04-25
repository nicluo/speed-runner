from .ui import SRWindow

class SpeedRunner():
    """
    Python application - Stopwatch and Timer.
    """
    def __init__(self):
        self.app = SRWindow()
        self.app.mainloop()
