import os
import sys
import Tkinter as tk
import ttk
import time
from PIL import Image, ImageTk, ImageFont, ImageDraw
from ..lib.stopwatch import StopWatch

BASE_DIR = sys._MEIPASS if getattr( sys, 'frozen', False ) else ''
APP_WIDTH = 180
APP_HEIGHT = 180
PADDING = 50

class SRWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.windowConfig()
        self.fixToTopRight()
        self.frame = BorderedFrame(self)
        self.frame.pack()
        self.redButton = RedButton(self.frame)
        self.redButton.place(bordermode='inside', x=(APP_WIDTH-100)/2,  y=15)
        self.redButton.bind("<<Click>>", self.onTrigger)
        self.numberDisplay = NumberDisplay(self.frame)
        self.numberDisplay.place(bordermode='inside', x=(APP_WIDTH-160)/2,  y=125)
        self.stopWatch = StopWatch()
        self.onUpdate()

    def windowConfig(self):
        self.overrideredirect(1)
        self.lift()
        self.wm_attributes("-topmost", 1)

    def fixToTopRight(self):
        screenWidth = self.winfo_screenwidth()
        left = "+" + str(screenWidth-PADDING-APP_WIDTH)
        top = "+" + str(PADDING)
        self.geometry(left + top)

    def onTrigger(self, event):
        self.stopWatch.Toggle()

    def onUpdate(self):
        self.numberDisplay.SetTime(self.stopWatch.Read())
        self.after(100, self.onUpdate)

class BorderedFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        outerCanvas = tk.Canvas(self, bg="red", width=APP_WIDTH, height=APP_HEIGHT)
        outerCanvas.pack()
        innerCanvas = tk.Canvas(self, width=APP_WIDTH-14, height=APP_HEIGHT-14)
        innerCanvas.place(bordermode='inside', x=7,  y=7)

class NumberDisplay(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.width = 160
        self.height = 40
        self.fontSize = 30
        self.canvasImage = None
        self.config(width=self.width, height=self.height)
        self.seconds = None;
        self.SetTime(0)

    def SetTime(self, seconds):
        secondsFloor = int(seconds)
        if(self.seconds == secondsFloor):
            return
        self.seconds = secondsFloor

        if secondsFloor % 2:
            format = '%H %M %S'
        else:
            format = '%H:%M:%S'
        timeString = time.strftime(format, time.gmtime(secondsFloor))

        self.image = self.timeToImage(timeString)
        if self.canvasImage:
            self.delete(self.canvasImage)
        self.canvasImage = self.create_image(82, 25, image=self.image)

    def timeToImage(self, timeString):
        W, H = (self.width, self.height)
        image = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(BASE_DIR, "assets/fonts/DSEG/fonts/DSEG7-Modern/DSEG7Modern-BoldItalic.ttf"), self.fontSize)
        w, h = draw.textsize(timeString, font=font)
        draw.text(((W-w)/2,(H-h)/2), "88:88:88", font=font, fill=(240, 240, 240))
        draw.text(((W-w)/2,(H-h)/2), timeString, font=font, fill=(245, 29, 31))
        return ImageTk.PhotoImage(image)


class RedButton(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.image = self.loadButtonImage(os.path.join(BASE_DIR, "assets/images/button.jpg"))
        self.enterImage = self.loadButtonImage(os.path.join(BASE_DIR, "assets/images/button-hover.jpg"))
        self.clickImage = self.loadButtonImage(os.path.join(BASE_DIR, "assets/images/button-down.jpg"))
        self.enterCanvasImage = None
        self.clickCanvasImage = None

        self.config(width="100", height="100")
        self.create_image(50, 50, image=self.image)
        self.bind("<Button-1>", self.onClick)
        self.bind("<ButtonRelease-1>", self.onRelease)
        self.bind("<Enter>", self.onEnter)
        self.bind("<Leave>", self.onLeave)

    def loadButtonImage(self, path):
        image = Image.open(path)
        image = image.resize((90, 90), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

    def onClick(self, event):
        self.clickCanvasImage = self.create_image(50, 50, image=self.clickImage)

    def onRelease(self, event):
        self.delete(self.clickCanvasImage)
        self.clickCanvasImage = None
        self.event_generate("<<Click>>", when="tail")

    def onEnter(self, event):
        # This check lets a long click take precedence
        if not self.clickCanvasImage:
            self.enterCanvasImage = self.create_image(50, 50, image=self.enterImage)

    def onLeave(self, event):
        if self.enterCanvasImage:
            self.delete(self.enterCanvasImage)
