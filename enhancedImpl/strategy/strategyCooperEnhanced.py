import tkinter as tk
from tkinter import Canvas, Toplevel, LEFT, RIGHT, mainloop

def read_data_file(filepath="data.txt"):
    xvals, yvals = [], []
    with open(filepath, "r") as f:
        for line in f:
            parts = line.split()
            xvals.append(float(parts[0]))
            yvals.append(float(parts[1]))
    return xvals, yvals

def find_bounds(xvals, yvals):
    return min(xvals), max(xvals), 0, max(yvals)

def calc_scale(width, height, minx, maxx, miny, maxy):
    xfactor = (0.9 * width) / (maxx - minx)
    yfactor = (0.9 * height) / (maxy - miny)
    xpmin = int(0.05 * width)
    ypmin = int(0.05 * height)
    return xfactor, yfactor, xpmin, ypmin

def line_plot(canvas, width, height, xvals, yvals):
    minx, maxx, miny, maxy = find_bounds(xvals, yvals)
    xfactor, yfactor, xpmin, ypmin = calc_scale(width, height, minx, maxx, miny, maxy)
    coords = []
    for x, y in zip(xvals, yvals):
        px = (x - minx) * xfactor + xpmin
        py = height - (y - miny) * yfactor
        coords.extend((px, py))
    canvas.create_line(coords, fill="black")

def bar_plot(canvas, width, height, xvals, yvals):
    minx, maxx, miny, maxy = find_bounds(xvals, yvals)
    xfactor, yfactor, xpmin, ypmin = calc_scale(width, height, minx, maxx, miny, maxy)
    colors = ['red', 'green', 'blue', 'orange', 'gray']
    for i, (x, y) in enumerate(zip(xvals, yvals)):
        px = (x - minx) * xfactor + xpmin
        py = height - (y - miny) * yfactor
        color = colors[i % len(colors)]
        canvas.create_rectangle(px - 10, height, px + 10, py, fill=color)

def show_plot(plot_func, title):
    xvals, yvals = read_data_file()
    w, h = 300, 200
    top = Toplevel()
    top.title(title)
    canvas = Canvas(top, width=w, height=h)
    canvas.pack()
    plot_func(canvas, w, h, xvals, yvals)

class Builder:
    def build(self):
        root = tk.Tk()
        root.geometry("200x50")
        root.title("Strategy with First-Class Functions")

        line_button = tk.Button(root, text="Line plot",
            command=lambda: show_plot(line_plot, "Line Plot"))
        line_button.pack(side=LEFT, padx=10)

        bar_button = tk.Button(root, text="Bar plot",
            command=lambda: show_plot(bar_plot, "Bar Plot"))
        bar_button.pack(side=RIGHT, padx=10)

        mainloop()

def main():
    Builder().build()

if __name__ == "__main__":
    main()
