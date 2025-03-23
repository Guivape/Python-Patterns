import tkinter as tk
from tkinter import Canvas, NW

class ImageCanvas:
    def build(self):
        root = tk.Tk()
        root.title("Kiko")
        w, h = 516, 400
        root.configure(background='grey')
        
        path = "kiko.png"
        self.photoImg = tk.PhotoImage(file=path)

        # Draw on the canvas
        self.canv = Canvas(root, width=w + 40, height=h + 40)
        self.canv.pack(side="bottom", fill="both", expand="yes")
        self.canv.create_rectangle(20, 20, w + 20, h + 20, width=3)
        self.canv.create_image(20, 20, anchor=NW, image=self.photoImg)

        tk.mainloop()

def main():
    ImageCanvas().build()

if __name__ == "__main__":
    main()
