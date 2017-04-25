import os
import sys
import Tkinter as tk
from PIL import Image, ImageTk

BASE_DIR = sys._MEIPASS if getattr( sys, 'frozen', False ) else ''
BUTTON = 'assets/images/button.jpg'
BUTTON_ENTER = 'assets/images/button-hover.jpg'
BUTTON_CLICK = 'assets/images/button-down.jpg'

class RedButton(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.load_images()
        self.enter_overlay = None
        self.click_overlay = None

        self.config(width="100", height="100")
        self.create_image(50, 50, image=self.image)
        self.bind_events()

    def load_images(self):
        self.image = self.load_button_image(os.path.join(BASE_DIR, BUTTON))
        self.enter_image = self.load_button_image(os.path.join(BASE_DIR, BUTTON_ENTER))
        self.click_image = self.load_button_image(os.path.join(BASE_DIR, BUTTON_CLICK))

    def load_button_image(self, path):
        image = Image.open(path)
        image = image.resize((90, 90), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def bind_events(self):
        self.bind("<Button-1>", self.handle_click)
        self.bind("<ButtonRelease-1>", self.handle_release)
        self.bind("<Enter>", self.handle_enter)
        self.bind("<Leave>", self.handle_leave)

    def handle_click(self, event):
        self.click_overlay = self.create_image(50, 50, image=self.click_image)

    def handle_release(self, event):
        self.delete(self.click_overlay)
        self.click_overlay = None
        self.event_generate("<<Click>>", when="tail")

    def handle_enter(self, event):
        # This check lets a long click take precedence
        if self.click_overlay is None:
            self.enter_overlay = self.create_image(50, 50, image=self.enter_image)

    def handle_leave(self, event):
        if self.enter_overlay is not None:
            self.delete(self.enter_overlay)
