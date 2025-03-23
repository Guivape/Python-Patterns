import os
import tkinter as tk
from tkinter import Canvas, Listbox, Frame, Entry, LabelFrame, END, NW
from tkinter.ttk import Button, Style

# A simple exception to indicate that a handler couldn't process the message
class NotHandled(Exception):
    pass

def handle_request(message, handlers):
    for handler in handlers:
        try:
            handler(message)
            # done once handled
            return
        except NotHandled:
            # move on to the next handler
            continue

############################
# Handler functions
############################


def file_handler_factory(listbox):
    files = os.listdir('.')
    # fill listbox once
    listbox.delete(0, END)
    for f in files:
        listbox.insert(END, f)

    def _file_handler(message: str):
        found = False
        for idx, fname in enumerate(files):
            if message == fname.lower():
                listbox.selection_set(idx)
                found = True
        if not found:
            raise NotHandled
    return _file_handler

def color_handler_factory(frame):
    color_set = {"white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"}
    style = Style()

    def _color_handler(message: str):
        if message in color_set:
            style.configure('Color.TFrame', background=message)
            frame.config(style='Color.TFrame')
        else:
            raise NotHandled
    return _color_handler

def error_handler_factory(listbox):
    def _error_handler(message: str):
        # If it reaches here, no one handled it
        listbox.insert(END, message)
    return _error_handler

############################
# UI Classes
############################

class EntryChain(LabelFrame):
    def __init__(self, parent, handlers):
        super().__init__(parent, text="Enter command", borderwidth=3)
        self.handlers = handlers
        self.entry = Entry(self)
        self.entry.pack(pady=10, padx=10)
        self.send_button = Button(self, text="Send", command=self.on_send)
        self.send_button.pack()

    def on_send(self):
        message = self.entry.get().lower().strip()
        self.entry.delete(0, END)
        handle_request(message, self.handlers)


class Builder:
    def build(self):
        root = tk.Tk()
        root.geometry("425x350")
        root.title("Chain of Responsibility Demo")
        style = Style()
        style.theme_use('alt')

        # Canvas for images
        self.image_canvas = Canvas(root, width=150, height=200, bg="white")
        self.image_canvas.grid(row=0, column=0)

        # Listbox for files
        self.file_listbox = Listbox(root, height=10)
        self.file_listbox.grid(row=0, column=1)

        # Frame for color
        self.color_frame = Frame(root, width=100, height=100, relief=tk.RAISED)
        self.color_frame.grid(row=1, column=1, padx=5, pady=5)

        # Listbox for errors
        self.error_listbox = Listbox(root, height=10)
        self.error_listbox.grid(row=0, column=2)

        # The chain is now just a list of handler functions
        self.chain_handlers = [
            file_handler_factory(self.file_listbox),
            color_handler_factory(self.color_frame),
            error_handler_factory(self.error_listbox)
        ]

        # An entry chain for user input
        self.entry_chain = EntryChain(root, self.chain_handlers)
        self.entry_chain.grid(row=1, column=0, pady=30)

        root.mainloop()

def main():
    Builder().build()

if __name__ == "__main__":
    main()
