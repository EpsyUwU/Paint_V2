import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint V2")
        self.root.geometry("600x400")

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack()

        self.current_tool = None
        self.start_x, self.start_y = None, None
        self.image = np.full((400, 600, 3), (255, 255, 255), np.uint8)

        # Botones flotantes (dentro del lienzo)
        self.create_tool_button("Línea", self.draw_line, x=10, y=10)
        self.create_tool_button("Polilínea", self.draw_polyline, x=50, y=10)
        self.create_tool_button("Rectángulo", self.draw_rectangle, x=110, y=10)
        self.create_tool_button("Círculo", self.draw_circle, x=190, y=10)
        self.create_tool_button("Borrar", self.erase_area, x=250, y=10)

    def create_tool_button(self, text, command, x, y):
        button = tk.Button(self.canvas, text=text, command=command, bg="lightgray", activebackground="gray", borderwidth=0)
        button_window = self.canvas.create_window(x, y, anchor="nw", window=button)

    def draw_line(self):
        self.current_tool = "line"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)
    def draw_polyline(self):
        self.current_tool = "polyline"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def draw_rectangle(self):
        self.current_tool = "rectangle"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def draw_circle(self):
        self.current_tool = "circle"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def erase_area(self):
        self.current_tool = "erase"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def start_drawing(self, event):
        self.start_x, self.start_y = event.x, event.y

    def draw(self, event):
        # Limpiar el lienzo antes de dibujar la forma actual
        self.canvas.delete("current_shape")

        if self.current_tool == "line":
            if self.start_x is not None and self.start_y is not None:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="blue", width=2,tags="current_shape")
        elif self.current_tool == "polyline":
            if self.start_x is not None and self.start_y is not None:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="blue", width=2,tags="current_shape")
                self.start_x, self.start_y = event.x, event.y
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="green", width=2,tags="current_shape")
        elif self.current_tool == "circle":
            radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            self.canvas.create_oval(self.start_x - radius, self.start_y - radius, self.start_x + radius,
                                    self.start_y + radius, outline="red", width=2, tags="current_shape")
        elif self.current_tool == "erase":
            self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="white", outline="white",tags="current_shape")

    def update_canvas(self):
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)  # Convertir la imagen de PIL a ImageTk
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.img_tk = img_tk

    def end_drawing(self, event):
        if self.current_tool in ["line", "rectangle", "circle"]:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.start_x, self.start_y = None, None  # Restablecer los puntos de inicio


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

