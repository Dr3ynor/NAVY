import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk

class FractalLandscape:
    def __init__(self, iterations, roughness):
        self.iterations = iterations
        self.roughness = roughness
        self.size = 2**iterations + 1
        self.height_map = np.zeros((self.size, self.size))
    
    def generate(self):
        # Initialize corners
        size = self.size - 1
        self.height_map[0, 0] = np.random.normal(0, 1)
        self.height_map[0, size] = np.random.normal(0, 1)
        self.height_map[size, 0] = np.random.normal(0, 1)
        self.height_map[size, size] = np.random.normal(0, 1)
        
        # Iteratively subdivide
        step = size
        roughness = self.roughness
        while step > 1:
            half = step // 2
            
            # Diamond step
            for x in range(0, self.size - 1, step):
                for y in range(0, self.size - 1, step):
                    avg = (self.height_map[x, y] + 
                           self.height_map[x + step, y] + 
                           self.height_map[x, y + step] + 
                           self.height_map[x + step, y + step]) / 4.0
                    
                    self.height_map[x + half, y + half] = avg + np.random.normal(0, roughness)
            
            # Square step
            for x in range(0, self.size - 1, half):
                for y in range((x + half) % step, self.size - 1, step):
                    avg = 0
                    count = 0
                    
                    if x >= half:
                        avg += self.height_map[x - half, y]
                        count += 1
                    if x + half < self.size:
                        avg += self.height_map[x + half, y]
                        count += 1
                    if y >= half:
                        avg += self.height_map[x, y - half]
                        count += 1
                    if y + half < self.size:
                        avg += self.height_map[x, y + half]
                        count += 1
                        
                    avg /= count
                    self.height_map[x, y] = avg + np.random.normal(0, roughness)
            
            step = half
            roughness *= 0.5
            
        return self.height_map

class FractalLandscapeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Landscape Generator")
        

        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill="x")
        

        ttk.Label(input_frame, text="Iterations:").grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.iterations_var = tk.StringVar(value="6")
        ttk.Entry(input_frame, textvariable=self.iterations_var, width=10).grid(column=1, row=0, padx=5, pady=5, sticky="w")
        
        ttk.Label(input_frame, text="Roughness:").grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.roughness_var = tk.StringVar(value="1.0")
        ttk.Entry(input_frame, textvariable=self.roughness_var, width=10).grid(column=1, row=1, padx=5, pady=5, sticky="w")
        

        ttk.Button(input_frame, text="Generate", command=self.generate_landscape).grid(column=2, row=0, rowspan=2, padx=10, pady=5)
        

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        

        self.generate_landscape()
    
    def generate_landscape(self):
        try:
            iterations = int(self.iterations_var.get())
            print(f"ITERATIONS: {iterations}")
            roughness = float(self.roughness_var.get())
            
            if iterations < 1:
                iterations = 1
            
            self.ax.clear()
            

            fractal = FractalLandscape(iterations, roughness)
            height_map = fractal.generate()
            
            x = np.linspace(0, 1, height_map.shape[0])
            y = np.linspace(0, 1, height_map.shape[1])
            X, Y = np.meshgrid(x, y)
            
            surf = self.ax.plot_surface(X, Y, height_map, cmap='terrain', linewidth=0, antialiased=True)
            
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Height')
            self.ax.set_title('Fractal Landscape')
            self.ax.set_zlim(-2, 2)

            self.canvas.draw()
            
        except ValueError:
            print("Please enter valid numbers for iterations and roughness")

if __name__ == "__main__":
    root = tk.Tk()
    app = FractalLandscapeApp(root)
    root.geometry("800x600")
    root.mainloop()
