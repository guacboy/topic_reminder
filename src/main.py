from util import Util, BACKGROUND_COLOR, FONT_TYPE
from tkinter import *
from PIL import ImageTk, Image
import json
import random

# starting menu
root = Tk()
root.title("Topic Reminder")
root.geometry("480x340")
root.config(bg=BACKGROUND_COLOR)

add_topic_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))
add_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))
start_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))
done_image = ImageTk.PhotoImage(Image.open("assets/done-button.png"))
done_hover_image = ImageTk.PhotoImage(Image.open("assets/done-button-hover.png"))
skip_image = ImageTk.PhotoImage(Image.open("assets/skip-button.png"))
skip_hover_image = ImageTk.PhotoImage(Image.open("assets/skip-button-hover.png"))
edit_image = ImageTk.PhotoImage(Image.open("assets/skip-button.png"))
edit_hover_image = ImageTk.PhotoImage(Image.open("assets/skip-button-hover.png"))

current_reminder_list = []
    
class App:
    # type your topics
    def create_topic_window(reminder_frame,
                            reminder_label,
                            is_edit: bool) -> None:
        global topic_window
        
        topic_window = Toplevel()
        topic_window.geometry("480x440")
        topic_window.config(bg=BACKGROUND_COLOR)
        
        topic_entry = Util.create_text(topic_window)
        topic_entry.pack()
        
        add_topic_button = Util.create_button(topic_window)
        add_topic_button.config(image=add_topic_image,
                                command=lambda: App.add_topic(topic_entry))
        add_topic_button.pack()
        
        # differentiates between standard topic window vs edit window
        if reminder_label != None:
            topic_entry.insert(END, reminder_label.cget("text"))
            
            add_topic_button.config(image=add_topic_image,
                                    command=lambda: App.edit_topic(reminder_frame,
                                                                   reminder_label,
                                                                   topic_entry,
                                                                   is_edit))
    
    # adds the inserted topic into topic.json
    def add_topic(topic_entry) -> None:
        with open("../data/topic.json", "r") as file:
            topic_list = json.load(file)
            
        # gets the topic entered and saves it into topic.json
        topic_list["topic"].append(topic_entry.get("1.0", END).strip())
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_list, file, indent=4)
        
        topic_entry.delete("0.0", END)
    
    def edit_topic(reminder_frame,
                   reminder_label,
                   topic_entry,
                   is_edit: bool) -> None:
        with open("../data/topic.json", "r") as file:
            topic_list = json.load(file)
        
        # finds the idx and replaces old topic with new topic
        topic_idx = topic_list["topic"].index(reminder_label.cget("text"))
        topic_list["topic"][topic_idx] = topic_entry.get("1.0", END).strip()
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_list, file, indent=4)
        
        # refreshes the window
        reminder_frame.pack_forget()
        App.display_reminder(is_edit)
        
        topic_window.destroy()
    
    # window for displaying the reminders
    def create_reminder_window(is_topic_list: bool) -> None:
        global reminder_window
        
        reminder_window = Toplevel()
        reminder_window.geometry("480x840")
        reminder_window.config(bg=BACKGROUND_COLOR)
        
        # ensures the current topics displayed is reset
        current_reminder_list.clear()
        App.display_reminder(is_topic_list)
        
    def display_reminder(is_topic_list: bool) -> None:
        if reminder_window.winfo_exists():
            with open("../data/topic.json", "r") as file:
                topic_list = json.load(file)
            
            while True:
                # checks to display out of order (general) or in order (topic list)
                if is_topic_list:
                    # probably O(n!) but it works
                    for topic in topic_list["topic"]:
                        reminder = topic
                        if reminder not in current_reminder_list:
                            current_reminder_list.append(reminder)
                            break
                    break
                else:
                    # chooses a random reminder from topic.json
                    reminder = random.choice(topic_list["topic"])
                    
                    # avoids displaying repeated topics
                    if reminder not in current_reminder_list:
                        current_reminder_list.append(reminder)
                        break
                    
            # creates a frame to group the reminder label and button options
            reminder_frame = Util.create_frame(reminder_window)
            reminder_frame.pack(fill="x")
            
            reminder_label = Util.create_label(reminder_frame)
            reminder_label.config(text=reminder)
            reminder_label.pack()
            
            # hovering makes the done/skip buttons appear
            reminder_frame.bind("<Enter>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, reminder_label, True))
            # otherwise, makes them disappear
            reminder_frame.bind("<Leave>", lambda e: App.toggle_reminder_option_button(e, reminder_frame, reminder_label, False))
            
            if len(current_reminder_list) < len(topic_list["topic"]):
                delay = 2000
                
                # changes delay if showing the list of topics
                if is_topic_list:
                    delay = 0
                
                root.after(delay, App.display_reminder, is_topic_list)
    
    # toggles done/skip buttons below a reminder
    def toggle_reminder_option_button(e,
                                      reminder_frame: str,
                                      reminder_label,
                                      is_active: bool) -> None:
        # if object does not exist, creates object
        
        # creates an option_frame within a reminder_frame to allow the
        # options to always be below and center of the labels
        if not hasattr(reminder_frame, "option_frame"):
            reminder_frame.option_frame = Util.create_frame(reminder_frame)
        
        # creates "done" button
        if not hasattr(reminder_frame.option_frame, "done_button"):
            reminder_frame.option_frame.done_button = Util.create_button(reminder_frame.option_frame)
            reminder_frame.option_frame.done_button.config(image=done_image,
                                              command=lambda: modify_json_file(reminder_label, is_delete=True, is_edit=False))
            reminder_frame.option_frame.done_button.bind("<Enter>", lambda e: toggle_hover_effect(e, "done_button", True,))
            reminder_frame.option_frame.done_button.bind("<Leave>", lambda e: toggle_hover_effect(e, "done_button", False))
            
        # creates "skip" button
        if not hasattr(reminder_frame.option_frame, "skip_button"):
            reminder_frame.option_frame.skip_button = Util.create_button(reminder_frame.option_frame)
            reminder_frame.option_frame.skip_button.config(image=skip_image,
                                              command=lambda: modify_json_file(reminder_label, is_delete=False, is_edit=False))
            reminder_frame.option_frame.skip_button.bind("<Enter>", lambda e: toggle_hover_effect(e, "skip_button", True))
            reminder_frame.option_frame.skip_button.bind("<Leave>", lambda e: toggle_hover_effect(e, "skip_button", False))
            
        # creates "edit" button
        if not hasattr(reminder_frame.option_frame, "edit_button"):
            reminder_frame.option_frame.edit_button = Util.create_button(reminder_frame.option_frame)
            reminder_frame.option_frame.edit_button.config(image=skip_image,
                                              command=lambda: modify_json_file(reminder_label, is_delete=False, is_edit=True))
            reminder_frame.option_frame.edit_button.bind("<Enter>", lambda e: toggle_hover_effect(e, "edit_button", True))
            reminder_frame.option_frame.edit_button.bind("<Leave>", lambda e: toggle_hover_effect(e, "edit_button", False))

        # checks if cursor is hovering over frame
        if is_active:
            reminder_frame.option_frame.done_button.pack(side=LEFT)
            reminder_frame.option_frame.skip_button.pack(side=LEFT)
            reminder_frame.option_frame.edit_button.pack()
            reminder_frame.option_frame.pack()
        else:
            reminder_frame.option_frame.pack_forget()
        
        # toggles button-hover effect
        def toggle_hover_effect(e,
                                button: str,
                                is_hover: bool) -> None:
            if is_hover:
                if button == "done_button":
                    reminder_frame.option_frame.done_button.config(image=done_hover_image)
                elif button == "skip_button":
                    reminder_frame.option_frame.skip_button.config(image=skip_hover_image)
                elif button == "edit_button":
                    reminder_frame.option_frame.edit_button.config (image=skip_hover_image)
            else:
                reminder_frame.option_frame.done_button.config(image=done_image)
                reminder_frame.option_frame.skip_button.config(image=skip_image)
                reminder_frame.option_frame.edit_button.config(image=skip_image)
        
        def modify_json_file(reminder_label,
                             is_delete: bool,
                             is_edit: bool) -> None:
            if not is_edit:
                reminder_frame.pack_forget()
            
            if is_delete or is_edit:
                with open("../data/topic.json", "r") as file:
                        topic_list = json.load(file)
                
                # deleting a topic
                if is_delete:
                    # finds the matching text and deletes it from topic.json
                    topic_list["topic"].remove(reminder_label.cget("text"))
                
                # edits a topic
                if is_edit:
                    App.create_topic_window(reminder_frame,
                                            reminder_label,
                                            is_edit)
                    
                with open("../data/topic.json", "w") as file:
                    json.dump(topic_list, file, indent=4)

# title
title_label = Util.create_label(root)
title_label.config(text="Topic Reminder",
                   font=(FONT_TYPE, 25))
title_label.pack(pady=(20, 0))

# creates the topic button where you can insert your topics
topic_button = Util.create_button(root)
topic_button.config(image=add_topic_image,
                    command=lambda: App.create_topic_window(None))
topic_button.pack(pady=(50, 0))

# creates the topic list button where you can view your topics
topic_button = Util.create_button(root)
topic_button.config(image=add_topic_image,
                    command=lambda: App.create_reminder_window(is_topic_list=True))
topic_button.pack(pady=(10, 0))

# creates the start button
start_button = Util.create_button(root)
start_button.config(image=add_topic_image,
                    command=lambda: App.create_reminder_window(is_topic_list=False))
start_button.pack(side=BOTTOM,
                  pady=(0, 20))

if __name__ == "__main__":
    root.mainloop()