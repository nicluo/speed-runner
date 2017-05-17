import sys
import os
import pygame

BASE_DIR = sys._MEIPASS if getattr( sys, 'frozen', False ) else ''
WAV_PATH = 'assets/sounds/ding.wav'

class Alarm():
    def __init__(self):
        self.path = os.path.join(BASE_DIR, WAV_PATH)
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.sound = pygame.mixer.Sound(self.path)

    def play(self):
        if not self.mixer.get_busy():
            self.sound.play(loops=-1)

    def stop(self):
        self.sound.stop()
