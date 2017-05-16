"""
Stopwatch with start, stop, split, reset functions
"""

from event import Event
from .timeinterval import TimeInterval

class StopWatch():
    def __init__(self):
        self.running = False
        self.sw = TimeInterval()
        self.splits = [TimeInterval()]
        self.on_state_change = Event()

    def read(self):
        return self.sw.seconds()

    def read_split(self):
        return self.splits[-1].seconds()

    def toggle(self):
        if self.running:
            self.sw.stop()
            self.splits[-1].stop()
        else:
            self.sw.start()
            self.splits[-1].start()
        self.running = not self.running
        self.on_state_change(self.running)

    def reset(self):
        if self.running: # do not reset when running
            pass
        else:
            self.sw = TimeInterval()
            self.splits = [TimeInterval()]
            self.on_state_change(self.running)

    def split_next(self):
        self.splits[-1].stop()
        self.splits.append(TimeInterval())
        if(self.running):
            self.splits[-1].start()

    def split_previous(self):
        if len(self.splits) > 1:
            self.splits[-1] += self.splits[-2]
            self.splits[-2] = self.splits[-1]
            self.splits.pop()
