
from tkinter import *

class Decorator(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(relief=FLAT)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, evt):
        self.configure(relief=RAISED)

    def on_leave(self, evt):
       self.configure(relief=FLAT)

class CButton(Decorator):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="C Button")

class DButton(Decorator):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="D Button")


class Builder():
    def build(self):
        root = Tk()
        root.geometry("200x100")
        root.title("Tk buttons")
        cbut = CButton(root)
        dbut = DButton(root)
        qbut = Button(root, text="Quit", command=quit)
        cbut.pack( pady=3)
        dbut.pack( pady=3)
        qbut.pack()


#----------------------------------
def main():
    Builder().build()
    mainloop()

if __name__== "__main__":
    main()