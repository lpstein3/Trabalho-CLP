import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ctypes
import os
import sys

lib_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'libmandel.so')
if not os.path.exists(lib_path):
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'libmandel.dll')
try:
    lib = ctypes.CDLL(lib_path)
except OSError:
    print("Erro ao carregar biblioteca")
    sys.exit(1)

lib.compute_mandelbrot.argtypes = [
    ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_double,
    ctypes.c_double, ctypes.c_int,
    ctypes.POINTER(ctypes.c_ubyte)
]

class BurningShipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Burning Ship Fractal - Clique para ampliar")

        # Parâmetros iniciais ajustados para destacar as "chamas"
        self.width = 600
        self.height = 600
        self.centerX = -0.5
        self.centerY = -0.6
        self.zoom = 1.0
        self.maxIter = 256

        # Frame de controles
        ctrl_frame = ttk.Frame(root, padding=10)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(ctrl_frame, text="Largura:").grid(row=0, column=0, padx=5)
        self.width_var = tk.StringVar(value=str(self.width))
        ttk.Entry(ctrl_frame, textvariable=self.width_var, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(ctrl_frame, text="Altura:").grid(row=0, column=2, padx=5)
        self.height_var = tk.StringVar(value=str(self.height))
        ttk.Entry(ctrl_frame, textvariable=self.height_var, width=8).grid(row=0, column=3, padx=5)

        ttk.Label(ctrl_frame, text="Centro X:").grid(row=0, column=4, padx=5)
        self.cx_var = tk.StringVar(value=str(self.centerX))
        ttk.Entry(ctrl_frame, textvariable=self.cx_var, width=10).grid(row=0, column=5, padx=5)

        ttk.Label(ctrl_frame, text="Centro Y:").grid(row=0, column=6, padx=5)
        self.cy_var = tk.StringVar(value=str(self.centerY))
        ttk.Entry(ctrl_frame, textvariable=self.cy_var, width=10).grid(row=0, column=7, padx=5)

        ttk.Label(ctrl_frame, text="Zoom:").grid(row=0, column=8, padx=5)
        self.zoom_var = tk.StringVar(value=str(self.zoom))
        ttk.Entry(ctrl_frame, textvariable=self.zoom_var, width=10).grid(row=0, column=9, padx=5)

        ttk.Label(ctrl_frame, text="Iterações:").grid(row=0, column=10, padx=5)
        self.iter_var = tk.StringVar(value=str(self.maxIter))
        ttk.Entry(ctrl_frame, textvariable=self.iter_var, width=6).grid(row=0, column=11, padx=5)

        self.render_btn = ttk.Button(ctrl_frame, text="Renderizar", command=self.render)
        self.render_btn.grid(row=0, column=12, padx=10)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.canvas.bind("<Button-1>", self.on_click)

        self.render()

    def render(self):
        try:
            w = int(self.width_var.get())
            h = int(self.height_var.get())
            cx = float(self.cx_var.get())
            cy = float(self.cy_var.get())
            zoom = float(self.zoom_var.get())
            max_iter = int(self.iter_var.get())
        except ValueError:
            return

        if w != self.width or h != self.height:
            self.canvas.config(width=w, height=h)
            self.width, self.height = w, h

        buffer = (ctypes.c_ubyte * (w * h * 3))()
        lib.compute_mandelbrot(w, h, cx, cy, zoom, max_iter, buffer)

        img = Image.frombuffer('RGB', (w, h), buffer, 'raw', 'RGB', 0, 1)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.current_cx = cx
        self.current_cy = cy
        self.current_zoom = zoom

    def on_click(self, event):
        w = self.width
        h = self.height
        cx = self.current_cx
        cy = self.current_cy
        zoom = self.current_zoom

        xmin = cx - 1.5 / zoom
        xmax = cx + 1.5 / zoom
        ymin = cy - 1.5 / zoom
        ymax = cy + 1.5 / zoom

        px = event.x
        py = event.y
        new_cx = xmin + px * (xmax - xmin) / w
        new_cy = ymin + (h - py) * (ymax - ymin) / h

        self.cx_var.set(f"{new_cx:.10f}")
        self.cy_var.set(f"{new_cy:.10f}")
        self.zoom_var.set(f"{zoom * 2:.2f}")
        self.render()

if __name__ == "__main__":
    root = tk.Tk()
    app = BurningShipApp(root)
    root.mainloop()