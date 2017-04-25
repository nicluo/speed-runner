import Tkinter as tk

class BorderedFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.outer_canvas = tk.Canvas(self, bg="black")
        self.outer_canvas.pack()
        self.inner_canvas = tk.Canvas(self)
        self.inner_canvas.place(bordermode='inside', x=7,  y=7)
        self.dimensions(self['width'], self['height'])

    def dimensions(self, width, height):
        self.outer_canvas.configure(width=width, height=height)
        self.inner_canvas.configure(width=width-14, height=height-14)

    def border(self, colour):
        self.outer_canvas.configure(bg=colour)
