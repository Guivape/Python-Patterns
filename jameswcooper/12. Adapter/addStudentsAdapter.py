import tkinter as tk
from tkinter import Entry, Button, Listbox, END
from tkinter.ttk import Treeview
from random import randint
from typing import Protocol

# Define a protocol to specify the adapter interface for Listbox-like behavior
class ListAdapterProtocol(Protocol):
    def getSelected(self) -> str: ...
    def deleteSelection(self) -> None: ...
    def insertAtEnd(self, text: str) -> None: ...
    def grid(self, **kwargs) -> None: ...

# Adapter function to wrap objects dynamically to conform to ListAdapterProtocol
def listbox_adapter(obj) -> ListAdapterProtocol:
    class Adapter:
        def __init__(self, obj):
            self._obj = obj  # Store reference to wrapped object

        def getSelected(self):
            if isinstance(self._obj, Treeview):
                selected_item = self._obj.focus()
                return self._obj.item(selected_item).get("text", "")
            return self._obj.get(self._obj.curselection()[0])

        def deleteSelection(self):
            if isinstance(self._obj, Treeview):
                self._obj.delete(self._obj.focus())
            else:
                self._obj.delete(self._obj.curselection()[0])

        def insertAtEnd(self, text):
            if isinstance(self._obj, Treeview):
                # Insert text with random IQ and Score in the Treeview
                self._obj.insert("", "end", text=text, values=(Randint.getIQ(), Randint.getScore()))
            else:
                self._obj.insert(END, text)

        # Pass-through for grid and other methods
        def grid(self, **kwargs):
            self._obj.grid(**kwargs)

    return Adapter(obj)

# Button base class for reusable button command structure
class DButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, command=self.comd, **kwargs)
    
    def comd(self):
        pass

# Custom buttons to handle specific commands
class EntryButton(DButton):
    def __init__(self, root, buildui, **kwargs):
        super().__init__(root, text="Enter", **kwargs)
        self.buildui = buildui
    
    def comd(self):
        entry = self.buildui.getEntry()
        text = entry.get()
        leftList = self.buildui.getLeftList()
        leftList.insertAtEnd(text)
        entry.delete(0, END)

class MoveButton(DButton):
    def __init__(self, root, buildui, **kwargs):
        super().__init__(root, text="Move-->", **kwargs)
        self.buildui = buildui

    def comd(self):
        leftList = self.buildui.getLeftList()
        sel_text = leftList.getSelected()
        rightList = self.buildui.getRightList()
        rightList.insertAtEnd(sel_text)
        leftList.deleteSelection()

class RestoreButton(DButton):
    def __init__(self, root, buildui, **kwargs):
        super().__init__(root, text="<--Restore", **kwargs)
        self.buildui = buildui

    def comd(self):
        rightList = self.buildui.getRightList()
        sel_text = rightList.getSelected()
        leftList = self.buildui.getLeftList()
        leftList.insertAtEnd(sel_text)
        rightList.deleteSelection()

# Randint class for generating random IQ and score values
class Randint:
    @staticmethod
    def getIQ():
        return randint(115, 145)
    
    @staticmethod
    def getScore():
        return randint(25, 35)

# UI Builder class to assemble the application interface
class BuildUI:
    def __init__(self, root):
        self.root = root
        self.leftList = listbox_adapter(Listbox(root))
        self.rightList = listbox_adapter(Treeview(root, columns=("IQ", "Score")))

    def build(self):
        self.root.geometry("400x200")
        self.root.title("Two Lists Adapter Example")

        # Entry widget
        self.entry = Entry(self.root)
        self.entry.grid(row=0, column=0)

        # Listbox (left list)
        self.leftList.grid(row=1, column=0, rowspan=4)

        # Buttons
        EntryButton(self.root, self).grid(row=0, column=1, sticky="W")
        MoveButton(self.root, self).grid(row=1, column=1)
        RestoreButton(self.root, self).grid(row=2, column=1)

        # Treeview (right list) setup with explicit "Name" column
        self.rightList._obj.heading("#0", text="Name")
        self.rightList._obj.column("#0", width=100)
        self.rightList._obj.heading("IQ", text="IQ")
        self.rightList._obj.column("IQ", width=50)
        self.rightList._obj.heading("Score", text="Score")
        self.rightList._obj.column("Score", width=50)
        self.rightList.grid(row=1, column=2, rowspan=4)

    # Accessor methods for widgets
    def getRightList(self):
        return self.rightList

    def getLeftList(self):
        return self.leftList

    def getEntry(self):
        return self.entry

# Program entry point
def main():
    root = tk.Tk()
    app = BuildUI(root)
    app.build()
    root.mainloop()

if __name__ == "__main__":
    main()
