import tkinter as tk
from tkinter import ttk, messagebox, Listbox, END, NO
import random

############################
# METACLASS & REGISTRY
############################

class EventMeta(type):
    """
    A metaclass that auto-registers any subclass of BaseSwimEvent
    in a global EVENT_REGISTRY, removing the need for explicit
    factory logic or if/else statements.
    """
    EVENT_REGISTRY = {}

    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)
        if name not in ("BaseSwimEvent", "StubSeeding"):
            EventMeta.EVENT_REGISTRY[name] = cls

def get_event_class(class_name):
    """
    Retrieve the event class from the registry by name.
    Returns None if not found.
    """
    return EventMeta.EVENT_REGISTRY.get(class_name, None)

############################
#STUB "SWIMSEEDING" SECTION
############################

class StubSeeding(metaclass=EventMeta):
    def __init__(self, filename, lanes):
        self.filename = filename
        self.lanes = lanes

    def getSwimmers(self):
        """
        Returns a list of swimmers with random data
        to demonstrate UI integration. Each 'swimmer' is a
        simple object with 'heat', 'lane', 'getName()', 'age', 'seedtime'.
        """
        swimmers = []
        for i in range(1, 7):
            # Create random data
            heat = 1
            lane = i
            name = f"Swimmer_{i}"
            age = random.randint(16, 30)
            seedtime = f"{random.uniform(20.0, 60.0):.2f}"
            swimmers.append(Swimmer(heat, lane, name, age, seedtime))
        return swimmers

class Swimmer:
    """Simple object to hold swimmer data for demonstration."""
    def __init__(self, heat, lane, name, age, seedtime):
        self.heat = heat
        self.lane = lane
        self._name = name
        self.age = age
        self.seedtime = seedtime

    def getName(self):
        return self._name

############################
# BASE & CONCRETE EVENTS
############################

class BaseSwimEvent(metaclass=EventMeta):
    """
    Abstract base for all swim event classes.
    Registered automatically by EventMeta, 
    but not intended to be instantiated directly.
    """
    def __init__(self, filename, lanes):
        self.filename = filename
        self.lanes = lanes

    def getSeeding(self):
        raise NotImplementedError("Subclasses must implement getSeeding()")

class TimedFinalEvent(BaseSwimEvent):
    def getSeeding(self):
        return StubSeeding(self.filename, self.lanes)

class PrelimEvent(BaseSwimEvent):
    def getSeeding(self):
        return StubSeeding(self.filename, self.lanes)


class BuildUI:
    """
    Replaces the hardcoded if/else logic with reflection-based
    instantiation using the metaclass registry.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Factory Method with Metaclass & Reflection")

    def evselect(self, evt):
        """
        Callback triggered when user selects an event in the left listbox.
        Dynamically creates the event class from EVENT_MAPPING,
        calls getSeeding(), and displays swimmers in the Treeview.
        """
        index_tuple = self.evlist.curselection()
        if not index_tuple:
            return
        i = int(index_tuple[0])

        EVENT_MAPPING = {
            0: ("TimedFinalEvent", "500free.txt"),
            1: ("PrelimEvent",     "100free.txt"),
        }

      
        event_class_name, filename = EVENT_MAPPING.get(i, ("TimedFinalEvent", "500free.txt"))
        event_cls = get_event_class(event_class_name)
        if not event_cls:
            messagebox.showerror("Error", f"No event class found for {event_class_name}")
            return

        # Instantiate the event (Factory Method via reflection)
        event = event_cls(filename, 6)
        seeding = event.getSeeding()
        swmrs = seeding.getSwimmers()

        self.swlist.delete(*self.swlist.get_children())

        row = 1
        for sw in swmrs:
            self.swlist.insert(
                "",
                row,
                text=str(sw.heat).strip(),
                values=(str(sw.lane), sw.getName(), str(sw.age), sw.seedtime)
            )
            row += 1

    def build(self):
        self.root.geometry("420x220")


        self.evlist = Listbox(self.root, height=2)
        self.evlist.insert(END, "500 Free")
        self.evlist.insert(END, "100 Free")
        self.evlist.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        self.evlist.bind('<<ListboxSelect>>', self.evselect)

        self.swlist = ttk.Treeview(self.root)
        self.swlist["columns"] = ("lane", "name", "age", "seed")
        self.swlist.column("#0", width=40, minwidth=10, stretch=NO)  # heat
        self.swlist.column("lane", width=30, stretch=NO)
        self.swlist.column("name", width=100, stretch=NO)
        self.swlist.column("age", width=40, stretch=NO)
        self.swlist.column("seed", width=50, stretch=NO)

        self.swlist.heading('#0',   text="H")
        self.swlist.heading('lane', text="L")
        self.swlist.heading('name', text="Name")
        self.swlist.heading("age",  text="Age")
        self.swlist.heading('seed', text="Seed")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10, "bold"))

        self.swlist.grid(row=0, column=1, sticky="nsew", pady=10)
        self.root.grid_columnconfigure(1, weight=1)

        # Make it resizable
        self.root.grid_rowconfigure(0, weight=1)

        tk.mainloop()

def main():
    root = tk.Tk()
    ui = BuildUI(root)
    ui.build()

if __name__ == "__main__":
    main()
