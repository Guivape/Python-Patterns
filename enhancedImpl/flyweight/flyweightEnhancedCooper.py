"""
Enhanced Flyweight Implementation in Python
Demonstrates how __new__() can enable object reuse,
eliminating the need for a separate Factory.
"""

from tkinter import Tk, Canvas, mainloop

class Folder:
    """Flyweight folder that reuses instances based on color and canvas."""

    _instances = {}
    W = 50
    H = 30

    def __new__(cls, color, canvas):
        # Key is tuple of (color, canvas_id)
        # This ensures we reuse the same Folder object per color/canvas.
        key = (color, id(canvas))
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance._color = color
            instance.canvas = canvas
            cls._instances[key] = instance
        return cls._instances[key]

    def draw(self, tx, ty, name):
        self.canvas.create_rectangle(tx, ty, tx + Folder.W, ty + Folder.H,
                                     fill="black")
        self.canvas.create_text(tx + 20, ty + Folder.H + 15, text=name)
        self.canvas.create_rectangle(tx + 1, ty + 1, tx + Folder.W - 1,
                                     ty + Folder.H - 1,
                                     fill=self._color)
        self.canvas.create_line(tx + 1, ty + Folder.H - 5, tx + Folder.W - 1,
                                ty + Folder.H - 5,
                                fill="#cccccc")
        self.canvas.create_line(tx, ty + Folder.H + 1, tx + Folder.W - 1,
                                ty + Folder.H + 1, fill="black")
        self.canvas.create_line(tx + Folder.W + 1, ty, tx + Folder.W + 1,
                                ty + Folder.H, fill="black")
        self._draw_tab(tx, ty)
        self.canvas.create_line(tx + 1, ty + 1, tx + Folder.W - 1,
                                ty + 1, fill="#ffffff")
        self.canvas.create_line(tx + 1, ty + 1, tx + 1, ty + Folder.H - 1,
                                fill="#ffffff")

    def _draw_tab(self, tx, ty):
        """Draws the folder tab above the rectangle."""
        tableft = 0
        tabheight = 4
        tabwidth = 20
        tabslant = 3
        self.canvas.create_polygon(
            tx + tableft, ty,
            tx + tableft + tabslant, ty - tabheight,
            tx + tabwidth - tabslant, ty - tabheight,
            tx + tabwidth,         ty,
            fill='black'
        )
        self.canvas.create_polygon(
            tx + tableft + 1,          ty + 1,
            tx + tableft + tabslant+1, ty - tabheight + 1,
            tx + tabwidth - tabslant-1,ty - tabheight + 1,
            tx + tabwidth,            ty,
            fill=self._color
        )


class FlyCanvas:
    """
    Demonstrates the Flyweight pattern using __new__ for object reuse.
    Eliminates the old FolderFactory by allowing Folder itself to
    handle instance caching.
    """

    TOP = 30
    LEFT = 30
    HSPACE = 70
    VSPACE = 70
    ROWMAX = 2

    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x240")
        self.root.title("Folders with Flyweight")
        self.canvas = Canvas(self.root)
        self.canvas.bind('<Button-1>', self.mouse_click)
        self.canvas.pack()

        # Folder names
        self.namelist = ['Alan', 'Bonnie', 'Charlie', 'Donna',
                         'Edward', 'Fiametta', 'George']
        self.selectedName = 'Edward'

    def run(self):
        """Starts the Tkinter main loop."""
        self.repaint()
        self.root.mainloop()

    def repaint(self):
        """Draws all folders. Uses the same Folder object per color."""
        self.canvas.delete("all")  # Clear previous drawings
        x = FlyCanvas.LEFT
        row = FlyCanvas.TOP
        j = 0
        for nm in self.namelist:
            color = "#5f5f1c" if nm == self.selectedName else "yellow"
            folder = Folder(color, self.canvas)
            folder.draw(x, row, nm)
            x += FlyCanvas.HSPACE
            j += 1
            if j > FlyCanvas.ROWMAX:
                j = 0
                row += FlyCanvas.VSPACE
                x = FlyCanvas.LEFT

    def mouse_click(self, evt):
        """Checks if click is inside a folder; updates selected folder accordingly."""
        self.selectedName = ""
        found = False
        j = 0
        row = FlyCanvas.TOP
        x = FlyCanvas.LEFT

        for nm in self.namelist:
            if x < evt.x < x + Folder.W and row < evt.y < row + Folder.H:
                self.selectedName = nm
                found = True

            x += FlyCanvas.HSPACE
            j += 1

            if j > FlyCanvas.ROWMAX:
                j = 0
                row += FlyCanvas.VSPACE
                x = FlyCanvas.LEFT

        self.repaint()


def main():
    app = FlyCanvas()
    app.run()


if __name__ == "__main__":
    main()
