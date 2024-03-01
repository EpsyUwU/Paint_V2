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
        self.buttons = []
        self.buttons.append(self.create_tool_button("Línea", self.draw_line, x=10, y=10))
        self.buttons.append(self.create_tool_button("Polilínea", self.draw_polyline, x=90, y=10))
        self.buttons.append(self.create_tool_button("Rectángulo", self.draw_rectangle, x=190, y=10))
        self.buttons.append(self.create_tool_button("Círculo", self.draw_circle, x=290, y=10))
        self.buttons.append(self.create_tool_button("Borrar", self.erase_area, x=390, y=10))

        # Mostrar la imagen inicial
        self.update_canvas()

    def create_tool_button(self, text, command, x, y):
        button = tk.Button(self.canvas, text=text, command=command, bg="lightgray", activebackground="gray", borderwidth=0)
        button_window = self.canvas.create_window(x, y, anchor="nw", window=button)
        return button_window

    def draw_line(self):
        self.hide_buttons()
        self.current_tool = "line"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def draw_polyline(self):
        self.hide_buttons()
        self.current_tool = "polyline"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def draw_rectangle(self):
        self.hide_buttons()
        self.current_tool = "rectangle"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def draw_circle(self):
        self.hide_buttons()
        self.current_tool = "circle"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def erase_area(self):
        self.hide_buttons()
        self.current_tool = "erase"
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def hide_buttons(self):
        for button in self.buttons:
            self.canvas.itemconfigure(button, state='hidden')

    def show_buttons(self):
        for button in self.buttons:
            self.canvas.itemconfigure(button, state='normal')

    def start_drawing(self, event):
        self.start_x, self.start_y = event.x, event.y

    def draw(self, event):
        if self.current_tool == "line":
            self.clear_canvas()  # Borra el lienzo antes de dibujar una nueva línea
            cv2.line(self.image, (self.start_x, self.start_y), (event.x, event.y), (255, 0, 0), 2)
            self.update_canvas()
        elif self.current_tool == "polyline":
            if self.start_x is not None and self.start_y is not None:
                cv2.line(self.image, (self.start_x, self.start_y), (event.x, event.y), (255, 0, 0), 2)
                self.start_x, self.start_y = event.x, event.y
                self.update_canvas()
        elif self.current_tool == "rectangle":
            self.clear_canvas()  # Borra el lienzo antes de dibujar un nuevo rectángulo
            cv2.rectangle(self.image, (self.start_x, self.start_y), (event.x, event.y), (0, 255, 0), 2)
            self.update_canvas()
        elif self.current_tool == "circle":
            self.clear_canvas()
            radio = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            cv2.circle(self.image, (self.start_x, self.start_y), int(radio), (0, 0, 255), 2)
            self.image = self.image.copy()
            self.update_canvas()
        elif self.current_tool == "erase":
            cv2.circle(self.image, (event.x, event.y), 5, (255, 255, 255), -1)
            self.update_canvas()

    def clear_canvas(self):
        self.image = np.full((400, 600, 3), (255, 255, 255), np.uint8)

    def update_canvas(self):
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)  # Convertir la imagen de PIL a ImageTk
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.img_tk = img_tk

    def end_drawing(self, event):
        self.show_buttons()
        if self.current_tool == "line":
            if self.start_x is not None and self.start_y is not None:
                cv2.line(self.image, (self.start_x, self.start_y), (event.x, event.y), (255, 0, 0), 2)
                self.start_x, self.start_y = None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
