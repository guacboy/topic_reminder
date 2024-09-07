from tkinter import *

BACKGROUND_COLOR = "#18181a"
FONT_COLOR = "#ffffff"
FONT_TYPE = "Roobert"

class Util:
    def create_button(window):
        return Button(window)
    
    def create_label(window):
        return Label(window,
                     font=FONT_TYPE)
    
    def create_text(window):
        return Text(window,
                    font=FONT_TYPE,
                    height=10)
    
    def create_frame(window):
        return Frame(window)