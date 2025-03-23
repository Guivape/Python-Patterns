import tkinter as tk
from tkinter import Canvas, Frame, PhotoImage, LEFT, mainloop, NSEW, EW

class Mediator:
    """
    Manages the drawing objects, the canvas, and current 'state' functionality.
    Replaces separate classes (PickState, RectState, etc.) with a function-based
    approach and a simple state string.
    """

    def __init__(self, canvas):
        self.canvas = canvas
        self.rectList = []
        self.selectRect = None
        self.current_state = "pick"  # default state
        self.buttons = []

        # Instead of separate classes for each state, store them as function dicts
        self.state_methods = {
            "pick": {
                "mouseDown": self.pick_mouse_down,
                "mouseDrag": self.pick_mouse_drag,
                "select": self.pick_select
            },
            "rect": {
                "mouseDown": self.rect_mouse_down,
                "mouseDrag": self.noop,
                "select": self.noop
            },
            "circ": {
                "mouseDown": self.circ_mouse_down,
                "mouseDrag": self.noop,
                "select": self.noop
            },
            "fill": {
                "mouseDown": self.fill_mouse_down,
                "mouseDrag": self.noop,
                "select": self.fill_select
            }
        }

    def buttonDown(self, evt):
        fn = self.state_methods[self.current_state]["mouseDown"]
        fn(evt)

    def drag(self, evt):
        fn = self.state_methods[self.current_state]["mouseDrag"]
        fn(evt)

    def selectState(self):
        fn = self.state_methods[self.current_state]["select"]
        fn()

    def setState(self, state_name):
        self.current_state = state_name

    # ======= STATES LOGIC BELOW (formerly separate classes) =======

    # Pick / Move logic
    def pick_mouse_down(self, evt):
        x, y = evt.x, evt.y
        for r in self.rectList:
            r.setSelected(False)

        for r in self.rectList:
            if r.contains(x, y):
                r.setSelected(True)
                r.drawHandles()
                self.selectRect = r

    def pick_mouse_drag(self, evt):
        if self.selectRect:
            self.selectRect.move(evt.x, evt.y)

    def pick_select(self):
        pass  # no special action

    # Rectangle creation logic
    def rect_mouse_down(self, evt):
        new_rect = Rectangle(evt.x, evt.y, self.canvas)
        self.rectList.append(new_rect)

        for r in self.rectList:
            if r.isSelected():
                r.setSelected(False)
                r.hideHandles()

        for r in self.rectList:
            if r.contains(evt.x, evt.y):
                r.setSelected(True)
                self.selectRect = r

    # Circle creation logic
    def circ_mouse_down(self, evt):
        new_circle = Circle(evt.x, evt.y, self.canvas)
        self.rectList.append(new_circle)

        for r in self.rectList:
            if r.isSelected():
                r.setSelected(False)
                r.hideHandles()

        for r in self.rectList:
            if r.contains(evt.x, evt.y):
                r.setSelected(True)
                self.selectRect = r

    # Fill logic
    def fill_mouse_down(self, evt):
        for r in self.rectList:
            if r.contains(evt.x, evt.y):
                r.fillObject()
                self.selectRect = r
                break

    def fill_select(self):
        if self.selectRect is not None:
            self.selectRect.fillObject()

    # For states that do nothing on drag, etc.
    def noop(self, evt):
        pass

    # Helpers
    def addButton(self, but):
        self.buttons.append(but)

    def unselectButtons(self):
        for but in self.buttons:
            but.deselect()

    def getRectlist(self):
        return self.rectList

    def clear(self):
        while len(self.rectList) > 0:
            obj = self.rectList.pop()
            obj.undo()

# Minimal Rectangle class
class Rectangle:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self._selected = False
        self.fillcol = 'black'
        self.handles = []

        self.crect = self.canvas.create_rectangle(x - 20, y - 15, x + 20, y + 15, outline=self.fillcol)
        self.createHandles(x, y)
        self.hideHandles()

    def createHandles(self, x, y):
        fillcol = self.fillcol
        coords = [
            (x - 22, y - 2, x - 18, y + 2),
            (x + 18, y - 2, x + 22, y + 2),
            (x - 2, y - 17, x + 2, y - 13),
            (x - 2, y + 17, x + 2, y + 13)
        ]
        for c in coords:
            h = self.canvas.create_rectangle(*c, fill=fillcol, state="hidden")
            self.handles.append(h)

    def move(self, x, y):
        oldx, oldy = self.x, self.y
        self.x, self.y = x, y
        deltax, deltay = x - oldx, y - oldy
        self.canvas.move(self.crect, deltax, deltay)
        for h in self.handles:
            self.canvas.move(h, deltax, deltay)

    def undo(self):
        self.canvas.delete(self.crect)
        for h in self.handles:
            self.canvas.delete(h)

    def drawHandles(self):
        if self._selected:
            for h in self.handles:
                self.canvas.itemconfigure(h, state="normal")

    def contains(self, x, y):
        return (self.x - 30 <= x <= self.x + 30) and (self.y - 20 <= y <= self.y + 20)

    def setSelected(self, val):
        self._selected = val

    def isSelected(self):
        return self._selected

    def hideHandles(self):
        for h in self.handles:
            self.canvas.itemconfigure(h, state="hidden")

    def fillObject(self):
        self.canvas.itemconfig(self.crect, fill='red')

# Circle is a subclass with same logic except it draws an oval
class Circle(Rectangle):
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self._selected = False
        self.fillcol = 'black'
        self.handles = []

        self.crect = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline=self.fillcol)
        self.createHandles(x, y)
        self.hideHandles()

# Minimal button classes
class Command:
    def comd(self): pass

class DButton(tk.Button, Command):
    def __init__(self, master, mediator, **kwargs):
        super().__init__(master, command=self.comd, **kwargs)
        self.mediator = mediator
        self.mediator.addButton(self)

    def select(self):
        self.config(relief=tk.SUNKEN)

    def deselect(self):
        self.config(relief=tk.RAISED)

class PickButton(DButton):
    def __init__(self, master, mediator):
        super().__init__(master, mediator)
        self.photo = PhotoImage(file="arrow.gif")
        self.config(image=self.photo)

    def comd(self):
        self.mediator.unselectButtons()
        self.select()
        self.mediator.setState("pick")

class RectButton(DButton):
    def __init__(self, master, mediator):
        super().__init__(master, mediator)
        self.photo = PhotoImage(file="rectforbutton.png")
        self.config(image=self.photo)

    def comd(self):
        self.mediator.unselectButtons()
        self.select()
        self.mediator.setState("rect")

class CircleButton(DButton):
    def __init__(self, master, mediator):
        super().__init__(master, mediator)
        self.photo = PhotoImage(file="circlebutton.png")
        self.config(image=self.photo)

    def comd(self):
        self.mediator.unselectButtons()
        self.select()
        self.mediator.setState("circ")

class FillButton(DButton):
    def __init__(self, master, mediator):
        super().__init__(master, mediator)
        self.photo = PhotoImage(file="redbutton.png")
        self.config(image=self.photo)

    def comd(self):
        self.mediator.unselectButtons()
        self.select()
        self.mediator.setState("fill")
        self.mediator.selectState()

class ClearButton(DButton):
    def __init__(self, master, mediator):
        super().__init__(master, mediator, text="Clr")

    def comd(self):
        self.mediator.clear()

class Builder:
    def build(self):
        root = tk.Tk()
        root.geometry("350x250")
        root.title("Dynamic State Demo")

        frame = tk.Frame(root)
        frame.grid(row=0, column=0, sticky=EW)

        canvas = tk.Canvas(root)
        canvas.grid(row=1, column=0, sticky=NSEW)

        med = Mediator(canvas)
        canvas.bind("<Button-1>", med.buttonDown)
        canvas.bind("<B1-Motion>", med.drag)

        pickButton = PickButton(frame, med)
        rectButton = RectButton(frame, med)
        circleButton = CircleButton(frame, med)
        fillButton = FillButton(frame, med)
        clearButton = ClearButton(frame, med)

        pickButton.pack(side="left", padx=5)
        rectButton.pack(side="left", padx=5)
        circleButton.pack(side="left", padx=5)
        fillButton.pack(side="left", padx=5)
        clearButton.pack(side="left", padx=20)

        mainloop()

def main():
    Builder().build()

if __name__ == "__main__":
    main()
