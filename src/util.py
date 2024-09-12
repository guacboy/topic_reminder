from tkinter import *

BACKGROUND_COLOR = "#18181a"
FONT_COLOR = "#ffffff"
FONT_TYPE = "Roobert"

class Util:
    def create_button(window):
        return Button(window,
                      bg=BACKGROUND_COLOR,
                      activebackground=BACKGROUND_COLOR,
                      bd=0,
                      relief=FLAT,
                      compound=CENTER)
    
    def create_label(window):
        return Label(window,
                     bg=BACKGROUND_COLOR,
                     fg=FONT_COLOR,
                     font=FONT_TYPE)
    
    def create_text(window):
        return Text(window,
                    height=10,
                    padx=20,
                    pady=20,
                    bg=BACKGROUND_COLOR,
                    fg=FONT_COLOR,
                    font=FONT_TYPE,
                    spacing3=10,
                    wrap=WORD)
    
    def create_frame(window):
        return Frame(window,
                     bg=BACKGROUND_COLOR)