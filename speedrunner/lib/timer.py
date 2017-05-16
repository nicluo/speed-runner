"""
Countdown Timer with per-second and per-minute increments, start, stop, reset
"""

from event import Event
from .timeinterval import TimeInterval

class Timer():
    def __init__(self):
        self.running = False
        self.ti = TimeInterval()
        self.setting = 0
        self.on_state_change = Event()

    def read(self):
        return max(self.setting - self.ti.seconds(), 0)

    def expired(self):
        return self.setting < self.ti.seconds()

    def toggle(self):
        if self.running:
            self.ti.stop()
        else:
            self.ti.start()
        self.running = not self.running
        if self.expired():
            self.reset()
        self.on_state_change(self.running)

    def reset(self):
        if self.running: # do not reset when running
            pass
        elif self.expired():
            self.ti = TimeInterval()
        else:
            self.ti = TimeInterval()
            self.setting = 0

    def increment(self, seconds):
        self.setting += seconds

    def decrement(self, seconds):
        self.setting = max(self.setting - seconds, 0)
