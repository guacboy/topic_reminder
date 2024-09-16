from util import Util, BACKGROUND_COLOR, FONT_TYPE
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import random

# starting menu
root = Tk()
root.title("Topic Reminder")
root.geometry("480x290")
root.config(bg=BACKGROUND_COLOR)

# main menu options
new_topic_image = ImageTk.PhotoImage(Image.open("assets/new-topic-button.png"))
new_topic_hover_image = ImageTk.PhotoImage(Image.open("assets/new-topic-button-hover.png"))
view_topic_image = ImageTk.PhotoImage(Image.open("assets/view-topic-button.png"))
view_topic_hover_image = ImageTk.PhotoImage(Image.open("assets/view-topic-button-hover.png"))
start_image = ImageTk.PhotoImage(Image.open("assets/start-button.png"))
start_hover_image = ImageTk.PhotoImage(Image.open("assets/start-button-hover.png"))
# adding new topics
add_topic_image = ImageTk.PhotoImage(Image.open("assets/add-topic-button.png"))
add_topic_hover_image = ImageTk.PhotoImage(Image.open("assets/add-topic-button-hover.png"))
# editing existing topics
done_edit_image = ImageTk.PhotoImage(Image.open("assets/done-edit-button.png"))
done_edit_hover_image = ImageTk.PhotoImage(Image.open("assets/done-edit-button-hover.png"))
# modifying current topic
done_image = ImageTk.PhotoImage(Image.open("assets/done-button.png"))
done_hover_image = ImageTk.PhotoImage(Image.open("assets/done-button-hover.png"))
skip_image = ImageTk.PhotoImage(Image.open("assets/skip-button.png"))
skip_hover_image = ImageTk.PhotoImage(Image.open("assets/skip-button-hover.png"))
edit_image = ImageTk.PhotoImage(Image.open("assets/edit-button.png"))
edit_hover_image = ImageTk.PhotoImage(Image.open("assets/edit-button-hover.png"))

image_dict = {
    new_topic_image: new_topic_hover_image,
    view_topic_image: view_topic_hover_image,
    add_topic_image: add_topic_hover_image,
    done_edit_image: done_edit_hover_image,
    start_image: start_hover_image,
    done_image: done_hover_image,
    skip_image: skip_hover_image,
    edit_image: edit_hover_image,
}

current_reminder_list = []
    
class App:
    # type your topics
    def create_topic_window(reminder_frame: Frame,
                            reminder_label: Label,
                            is_edit: bool) -> None:
        global topic_window
        
        topic_window = Toplevel()
        topic_window.geometry("480x380")
        topic_window.config(bg=BACKGROUND_COLOR)
        
        topic_entry = Util.create_text(topic_window)
        topic_entry.pack()
        
        add_topic_button = Util.create_button(topic_window)
        add_topic_button.config(image=add_topic_image,
                                command=lambda: App.add_topic(topic_entry))
        add_topic_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, add_topic_button, add_topic_image, True))
        add_topic_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, add_topic_button, add_topic_image, False))
        add_topic_button.pack(pady=(10, 0))
        
        # differentiates between standard topic window vs edit window
        if reminder_label != None:
            topic_entry.insert(END, reminder_label.cget("text"))
            
            done_edit_button = add_topic_button
            done_edit_button.config(image=done_edit_image,
                                    command=lambda: App.edit_topic(reminder_frame,
                                                                   reminder_label,
                                                                   topic_entry,
                                                                   is_edit))
            done_edit_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, done_edit_button, done_edit_image, True))
            done_edit_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, done_edit_button, done_edit_image, False))
    
    # adds the inserted topic into topic.json
    def add_topic(topic_entry: Text) -> None:
        with open("../data/topic.json", "r") as file:
            topic_list = json.load(file)
            
        # gets the topic entered and saves it into topic.json
        topic_list["topic"].append(topic_entry.get("1.0", END).strip())
        
        with open("../data/topic.json", "w") as file:
            json.dump(topic_list, file, indent=4)
        
        topic_entry.delete("0.0", END)
    
    def edit_topic(reminder_frame: Frame,
                   reminder_label: Label,
                   topic_entry: Text,
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
    def create_reminder_window(is_view_topic: bool) -> None:
        # displays an error if there aren't any topics in topic.json
        def show_error() -> None:
            messagebox.showerror("NO TOPICS FOUND", "Please add at least one topic.")
            new_topic_button.invoke()
            
        with open("../data/topic.json", "r") as file:
            topic_list = json.load(file)
        
        if len(topic_list["topic"]) > 0:
            global reminder_window
            
            reminder_window = Toplevel()
            reminder_window.geometry("480x840")
            reminder_window.config(bg=BACKGROUND_COLOR)
            
            # ensures the current topics displayed is reset
            current_reminder_list.clear()
            App.display_reminder(is_view_topic)
        else:
            show_error()
        
    def display_reminder(is_view_topic: bool) -> None:
        if reminder_window.winfo_exists():
            with open("../data/topic.json", "r") as file:
                topic_list = json.load(file)
            
            while True:
                # checks to display out of order (general) or in order (topic list)
                if is_view_topic:
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
                delay = 600000
                
                # changes delay if showing the list of topics
                if is_view_topic:
                    delay = 0
                    
                root.after(delay, App.display_reminder, is_view_topic)
    
    # toggles done/skip buttons below a reminder
    def toggle_reminder_option_button(e,
                                      reminder_frame: Frame,
                                      reminder_label: Label,
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
            reminder_frame.option_frame.done_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.done_button, done_image, True))
            reminder_frame.option_frame.done_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.done_button, done_image, False))
            
        # creates "skip" button
        if not hasattr(reminder_frame.option_frame, "skip_button"):
            reminder_frame.option_frame.skip_button = Util.create_button(reminder_frame.option_frame)
            reminder_frame.option_frame.skip_button.config(image=skip_image,
                                              command=lambda: modify_json_file(reminder_label, is_delete=False, is_edit=False))
            reminder_frame.option_frame.skip_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.skip_button, skip_image, True))
            reminder_frame.option_frame.skip_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.skip_button, skip_image, False))
            
        # creates "edit" button
        if not hasattr(reminder_frame.option_frame, "edit_button"):
            reminder_frame.option_frame.edit_button = Util.create_button(reminder_frame.option_frame)
            reminder_frame.option_frame.edit_button.config(image=edit_image,
                                              command=lambda: modify_json_file(reminder_label, is_delete=False, is_edit=True))
            reminder_frame.option_frame.edit_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.edit_button, edit_image, True))
            reminder_frame.option_frame.edit_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, reminder_frame.option_frame.edit_button, edit_image, False))

        # checks if cursor is hovering over frame
        if is_active:
            reminder_frame.option_frame.done_button.pack(side=LEFT)
            reminder_frame.option_frame.skip_button.pack(side=LEFT)
            reminder_frame.option_frame.edit_button.pack()
            reminder_frame.option_frame.pack()
        else:
            reminder_frame.option_frame.pack_forget()
        
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
    
    # toggles button-hover effect 
    def toggle_hover_effect(e,
                            button: Button,
                            image_type: PhotoImage,
                            is_hover: bool) -> None:
            if is_hover:
                button.config(image=image_dict[image_type])
            else:
                button.config(image=image_type)

# title
title_label = Util.create_label(root)
title_label.config(text="Topic Reminder",
                   font=(FONT_TYPE, 25))
title_label.pack(pady=(20, 0))

# creates the new topic button where you can insert your topics
new_topic_button = Util.create_button(root)
new_topic_button.config(image=new_topic_image,
                        command=lambda: App.create_topic_window(None, None, False))
new_topic_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, new_topic_button, new_topic_image, True))
new_topic_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, new_topic_button, new_topic_image, False))
new_topic_button.pack(pady=(20, 0))

# creates the view topic button where you can view your topics
view_topic_button = Util.create_button(root)
view_topic_button.config(image=view_topic_image,
                         command=lambda: App.create_reminder_window(is_view_topic=True))
view_topic_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, view_topic_button, view_topic_image, True))
view_topic_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, view_topic_button, view_topic_image, False))
view_topic_button.pack(pady=(10, 0))

# creates the start button
start_button = Util.create_button(root)
start_button.config(image=start_image,
                    command=lambda: App.create_reminder_window(is_view_topic=False))
start_button.bind("<Enter>", lambda e: App.toggle_hover_effect(e, start_button, start_image, True))
start_button.bind("<Leave>", lambda e: App.toggle_hover_effect(e, start_button, start_image, False))
start_button.pack(side=BOTTOM,
                  pady=(0, 20))

if __name__ == "__main__":
    root.mainloop()