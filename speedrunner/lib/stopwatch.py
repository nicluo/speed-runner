"""
Stopwatch with start, stop, split, reset functions
"""

import time
from event import Event

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
            self.splits[-2] = self.splits[-1] + self.splits[-2]
            self.splits.pop()

class TimeInterval():
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0

    def start(self):
        if not self.start_time:
            self.start_time = time.time()

    def stop(self):
        if self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def seconds(self):
        if self.start_time is not None:
            return self.elapsed_time + (time.time() - self.start_time)
        else:
            return self.elapsed_time

    def merge(self, ti):
        self.elapsed_time += ti.elapsed_time

    __iadd__ = merge
