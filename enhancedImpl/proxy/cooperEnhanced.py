import tkinter as tk
from tkinter import Canvas, NW

class ProxyPhotoImage(tk.PhotoImage):
    """
    A simple proxy that logs attribute access.
    Inherits from PhotoImage so Tkinter sees it as a real image object.
    We create the actual image right away (no lazy load).
    """

    def __init__(self, path):
        super().__init__(file=path)

    def __getattr__(self, name):
        # __getattr__ is called only if 'name' isn't found on the instance
        print(f"[Proxy] Accessing attribute '{name}'")
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            print(f"[Proxy] Setting attribute '{name}' to {value}")
            super().__setattr__(name, value)
        else:
            # For new attributes not in PhotoImage, store them on self
            print(f"[Proxy] Storing new attribute '{name}'={value}")
            object.__setattr__(self, name, value)


class ImageCanvas:
    def build(self):
        root = tk.Tk()
        root.title("Kiko - Proxy Demo")
        w, h = 516, 400
        root.configure(background='grey')

        # Use the ProxyPhotoImage rather than PhotoImage(file=...)
        self.photoImg = ProxyPhotoImage("kiko.png")

        canv = Canvas(root, width=w + 40, height=h + 40)
        canv.pack(side="bottom", fill="both", expand=True)
        canv.create_rectangle(20, 20, w + 20, h + 20, width=3)
        canv.create_image(20, 20, anchor=NW, image=self.photoImg)

        tk.mainloop()


def main():
    ImageCanvas().build()

if __name__ == "__main__":
    main()
