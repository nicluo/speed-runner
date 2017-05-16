"""
TimeInterval handles start stop actions to produce a seconds elapsed value
"""

import time

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
        return self

    __iadd__ = merge
