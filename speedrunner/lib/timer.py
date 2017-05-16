"""
Countdown Timer with per-second and per-minute increments, start, stop, reset
"""

from event import Event
from .timeinterval import TimeInterval

class Timer():
    def __init__(self):
        self.running = False
        self.sw = TimeInterval()
        self.setting = 0
        self.on_state_change = Event()

    def read(self):
        return self.setting - self.sw.seconds()

    def toggle(self):
        if self.running:
            self.sw.stop()
        else:
            self.sw.start()
        self.running = not self.running
        self.on_state_change(self.running)

    def reset(self):
        if self.running: # do not reset when running
            pass
        else:
            self.sw = TimeInterval()
            self.setting = 0
            self.on_state_change(self.running)

    def increment_second(self):
        self.setting += 1

    def increment_minute(self):
        self.setting += 60
