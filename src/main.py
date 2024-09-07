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

current_reminder_list = []
    
class App:
    # type your topics
    def create_topic_window():
        topic_window = Toplevel()
        topic_window.geometry("480x440")
        topic_window.config(bg=BACKGROUND_COLOR)
        
        topic_entry = Util.create_text(topic_window)
        topic_entry.pack()
        
        add_topic_button = Util.create_button(topic_window)
        add_topic_button.config(image=add_topic_image,
                                command=lambda: App.add_topic(topic_entry))
        add_topic_button.pack()
    
    # adds the inserted topic into topic.json
    def add_topic(topic_entry):
        with open("../data/topic.json", "r") as file:
            topic_list = json.load(file)
            
        # gets the topic entered and saves it into topic.json
        topic_list["topic"].append(topic_entry.get("1.0", END).strip())
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_list, file, indent=4, sort_keys=True)
        
        topic_entry.delete("0.0", END)
    
    # window for displaying the reminders
    def create_reminder_window():
        reminder_window = Toplevel()
        reminder_window.geometry("480x840")
        reminder_window.config(bg=BACKGROUND_COLOR)
        
        # ensures the current topics displayed is reset
        current_reminder_list.clear()
        App.display_reminder(reminder_window)
        
    def display_reminder(window):
        if window.winfo_exists():
            with open("../data/topic.json", "r") as file:
                topic_list = json.load(file)
            
            # chooses a random reminder from topic.json
            while True:
                reminder = random.choice(topic_list["topic"])
                
                # avoids displaying repeated topics
                if reminder not in current_reminder_list:
                    current_reminder_list.append(reminder)
                    break
            
            reminder_frame = Util.create_frame(window)
            reminder_frame.pack()
            
            reminder_label = Util.create_label(reminder_frame)
            reminder_label.config(text=reminder)
            reminder_label.pack()
            
            # hovering makes the done/skip buttons appear
            reminder_frame.bind("<Enter>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, reminder_label, True))
            # otherwise, makes them disappear
            reminder_frame.bind("<Leave>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, reminder_label, False))
            
            if len(current_reminder_list) < len(topic_list["topic"]):
                root.after(2000, App.display_reminder, window)
    
    # toggles done/skip buttons below a reminder
    def toggle_reminder_option_button(e,
                                      reminder_frame: str,
                                      reminder_label,
                                      is_active: bool):
        if not hasattr(reminder_frame, "skip_button"):
            reminder_frame.skip_button = Util.create_button(reminder_frame)
            reminder_frame.skip_button.config(image=add_topic_image,
                                              command=lambda: modify_json_file(reminder_label, False))
        
        if not hasattr(reminder_frame, "done_button"):
            reminder_frame.done_button = Util.create_button(reminder_frame)
            reminder_frame.done_button.config(image=add_topic_image,
                                              command=lambda: modify_json_file(reminder_label, True))

        # checks if cursor is hovering over frame
        if is_active:
            reminder_frame.skip_button.pack(side=LEFT)
            reminder_frame.done_button.pack()
        else:
            reminder_frame.skip_button.pack_forget()
            reminder_frame.done_button.pack_forget()
        
        def modify_json_file(reminder_label,
                             is_delete: bool):
            reminder_frame.pack_forget()
            
            if is_delete:
                with open("../data/topic.json", "r") as file:
                        topic_list = json.load(file)
                
                # finds the matching text and deletes it from topic.json
                topic_list["topic"].remove(reminder_label.cget("text"))
                    
                with open("../data/topic.json", "w") as file:
                    json.dump(topic_list, file, indent=4, sort_keys=True)

topic_button = Util.create_button(root)
topic_button.config(image=add_topic_image,
                    command=lambda: App.create_topic_window())
topic_button.place(anchor=CENTER,
                   relx=0.5,
                   rely=0.5)

start_button = Util.create_button(root)
start_button.config(image=add_topic_image,
                    command=lambda: App.create_reminder_window())
start_button.pack(side=BOTTOM)

if __name__ == "__main__":
    root.mainloop()