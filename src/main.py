from util import Util, BACKGROUND_COLOR
from tkinter import *
from PIL import ImageTk, Image
import json

# starting menu
root = Tk()
root.title("Topic Reminder")
root.geometry("480x540")
root.config(bg=BACKGROUND_COLOR)

add_topic_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))

class App:
    # type your topics
    def create_topic_window(request: str):
        topic_window = Toplevel()
        topic_window.geometry("480x440")
        topic_window.config(bg=BACKGROUND_COLOR)
        
        topic_entry = Util.create_text(topic_window)
        topic_entry.pack()
        
        add_topic_button = Util.create_button(topic_window)
        add_topic_button.config(image=add_topic_image,
                                command=lambda: App.add_topic(request,
                                                              topic_entry))
        add_topic_button.pack()
    
    # adds the inserted topic into topic.json
    def add_topic(request: str,
                  topic_entry):
        with open("../data/topic.json", "r") as file:
            topic_example = json.load(file)
        
        topic_example[request].append(topic_entry.get("1.0", END))
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_example, file, indent=4, sort_keys=True)
        
        topic_entry.delete("0.0", END)

topic_button = Util.create_button(root)
topic_button.config(text="add topic",
                    command=lambda: App.create_topic_window("topic"))
topic_button.pack()

if __name__ == "__main__":
    root.mainloop()