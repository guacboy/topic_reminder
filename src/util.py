from tkinter import *

BACKGROUND_COLOR = "#18181a"
FONT_COLOR = "#ffffff"
FONT_TYPE = "Roobert"

class Util:
    def create_button(window):
        return Button(window)
    
    def create_label(window):
        return Label(window)
    
    def create_text(window):
        return Text(window)