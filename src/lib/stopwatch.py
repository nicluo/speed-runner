import time

class StopWatch():
    def __init__(self):
        self.running = False
        self.startTime = None
        self.elapsedTime = 0
    def Toggle(self):
        if not self.startTime:
            self.running = True
            self.startTime = time.time()
        else:
            self.elapsedTime = self.Read()
            self.running = False
            self.startTime = None
    def Read(self):
        if self.running:
            return self.elapsedTime + (time.time() - self.startTime)
        else:
            return self.elapsedTime
