from util import Util, BACKGROUND_COLOR
from tkinter import *
from PIL import ImageTk, Image
import json
import random

# starting menu
root = Tk()
root.title("Topic Reminder")
root.geometry("480x540")
root.config(bg=BACKGROUND_COLOR)

add_topic_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))

current_topic_display = []
    
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
            topic_list = json.load(file)
        
        # gets the topic entered and saves it into topic.json
        topic_list[request].append(topic_entry.get("1.0", END))
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_list, file, indent=4, sort_keys=True)
        
        topic_entry.delete("0.0", END)
    
    # window for displaying the reminders
    def create_reminder_window():
        reminder_window = Toplevel()
        reminder_window.geometry("480x840")
        reminder_window.config(bg=BACKGROUND_COLOR)
        
        App.display_reminder(reminder_window)
        
    def display_reminder(window):
        if window.winfo_exists():
            with open("../data/topic.json", "r") as file:
                topic_list = json.load(file)
            
            # chooses a random reminder from topic.json
            while True:
                random_reminder = random.choice(topic_list["topic"])
                
                # avoids displaying repeated topics
                if random_reminder not in current_topic_display:
                    current_topic_display.append(random_reminder)
                    break
            
            # creates a random tag (variable)
            random_reminder_tag = "".join([random.choice("1234567890") for tag in range(6)])
            
            reminder_frame = Util.create_frame(window)
            reminder_frame.pack()
            
            random_reminder_tag = Util.create_label(reminder_frame)
            random_reminder_tag.config(text=random_reminder)
            random_reminder_tag.pack()
            
            # hovering makes the approve/decline buttons appear
            reminder_frame.bind("<Enter>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, True))
            # otherwise, makes them disappear
            reminder_frame.bind("<Leave>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, False))
            
            if len(current_topic_display) < len(topic_list["topic"]):
                root.after(3000, App.display_reminder, window)
    
    # toggles approve/decline buttons below a reminder
    def toggle_reminder_option_button(e,
                                      frame,
                                      active: bool):
        if not hasattr(frame, "approve_button"):
            frame.approve_button = Util.create_button(frame)
            frame.approve_button.config(image=add_topic_image, command=lambda: print("approve"))
        
        if not hasattr(frame, "decline_button"):
            frame.decline_button = Util.create_button(frame)
            frame.decline_button.config(image=add_topic_image, command=lambda: print("decline"))

        if active:
            frame.approve_button.pack(side=LEFT)
            frame.decline_button.pack()
        else:
            frame.approve_button.pack_forget()
            frame.decline_button.pack_forget()

topic_button = Util.create_button(root)
topic_button.config(image=add_topic_image,
                    command=lambda: App.create_topic_window("topic"))
topic_button.place(anchor=CENTER,
                   relx=0.5,
                   rely=0.5)

start_button = Util.create_button(root)
start_button.config(image=add_topic_image,
                    command=lambda: App.create_reminder_window())
start_button.pack(side=BOTTOM)

if __name__ == "__main__":
    root.mainloop()