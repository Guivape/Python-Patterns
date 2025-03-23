import tkinter as tk
from tkinter import Listbox, Frame, END, messagebox, LabelFrame, IntVar, Checkbutton
from tkinter.ttk import Button

class Securities:
    def __init__(self, name, sec_list):
        self.name = name
        self.sec_list = sec_list
    def getName(self):
        return self.name
    def getList(self):
        return self.sec_list

class MultiChoice:
    def makeUI(self): pass
    def getSelected(self): return []

class ListboxChoice(MultiChoice):
    def __init__(self, parent, items):
        self.parent = parent
        self.items = items
        self.listbox = None

    def makeUI(self):
        # Clear existing
        for w in self.parent.winfo_children():
            w.destroy()
        self.listbox = Listbox(self.parent, selectmode="multiple")
        self.listbox.pack()
        for item in self.items:
            self.listbox.insert(END, item)
        return self  # method chaining

    def getSelected(self):
        if not self.listbox:
            return []
        selected = self.listbox.curselection()
        return [self.listbox.get(i) for i in selected]

class CheckboxChoice(MultiChoice):
    def __init__(self, parent, items):
        self.parent = parent
        self.items = items
        self.boxes = []

    def makeUI(self):
        for w in self.parent.winfo_children():
            w.destroy()
        self.boxes = []
        for i, txt in enumerate(self.items):
            var = IntVar()
            cb = Checkbutton(self.parent, text=txt, variable=var)
            cb.pack(anchor="w")
            self.boxes.append((txt, var))
        return self  # method chaining

    def getSelected(self):
        return [txt for (txt, var) in self.boxes if var.get() == 1]

class ChoiceFactory:
    def getChoiceUI(self, items, parent):
        if len(items) > 3:
            return ListboxChoice(parent, items)
        else:
            return CheckboxChoice(parent, items)

class ShowButton(Button):
    def __init__(self, builder, parent):
        super().__init__(parent, text="Show")
        self.builder = builder
        self.config(command=self.on_click)

    def on_click(self):
        selection = self.builder.getSelected()
        messagebox.showinfo("Selected Securities", "\n".join(selection))

class BuildUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x250")
        self.root.title("Wealth Builder")
        self.securities = []
        self.choiceUI = None

    def loadData(self):
        self.securities = [
            Securities("Stocks", ["Cisco", "Coca Cola", "General Electric", "Harley-Davidson", "IBM"]),
            Securities("Bonds", ["CT State GO 2024", "New York GO 2026", "GE Corp Bonds"]),
            Securities("Mutuals", ["Fidelity Magellan", "T Rowe Price", "Vanguard Primecap", "Lindner"]),
        ]
        return self  # method chaining

    def buildLeftList(self):
        self.leftFrame = Frame(self.root)
        self.leftFrame.grid(row=0, column=0)
        self.leftList = Listbox(self.leftFrame, exportselection=False)
        self.leftList.pack()
        for sec in self.securities:
            self.leftList.insert(END, sec.getName())
        self.leftList.bind("<<ListboxSelect>>", self.onLeftSelect)
        return self

    def buildRightFrame(self):
        self.rightFrame = Frame(self.root)
        self.rightFrame.grid(row=0, column=1)
        return self

    def buildShowButton(self):
        self.showButton = ShowButton(self, self.root)
        self.showButton.grid(row=1, column=0, columnspan=2, pady=10)
        return self

    def onLeftSelect(self, evt):
        idx = self.leftList.curselection()
        if not idx:
            return
        index = idx[0]
        items = self.securities[index].getList()

        cf = ChoiceFactory()
        # Create the UI for the selected items
        self.choiceUI = cf.getChoiceUI(items, self.rightFrame).makeUI()

    def getSelected(self):
        if self.choiceUI:
            return self.choiceUI.getSelected()
        return []

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    builder = (
        BuildUI(root)
        .loadData()
        .buildLeftList()
        .buildRightFrame()
        .buildShowButton()
    )
    builder.run()

if __name__ == "__main__":
    main()
