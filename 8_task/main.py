import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

class FractalVisualizer:
    def __init__(self):
        self.max_iterations = 100
        self.x_min, self.x_max = -2.0, 1.0
        self.y_min, self.y_max = -1.5, 1.5
        self.resolution = 500
        self.fractal_type = "mandelbrot"
        self.c_real = -0.4
        self.c_imag = 0.6
        self.c = complex(self.c_real, self.c_imag)
        self.colormap = "hot"
        self.available_colormaps = ['hot', 'viridis', 'plasma', 'inferno', 'magma', 'jet']
        
        # Zoom factor
        self.zoom_factor = 0.5  # after each click, the zoom is 50% of the previous size
        

        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.35, top=0.95)
        

        self.create_fractal()
        
        ax_iterations = plt.axes([0.1, 0.25, 0.65, 0.03])
        self.slider_iterations = Slider(
            ax_iterations, 'Num. iterations', 10, 500, 
            valinit=self.max_iterations, valstep=10
        )
        self.slider_iterations.on_changed(self.update_from_slider)
        
        ax_reset = plt.axes([0.8, 0.25, 0.1, 0.03])
        self.button_reset = Button(ax_reset, 'Reset Zoom')
        self.button_reset.on_clicked(self.reset_zoom)
        
        ax_fractal_type = plt.axes([0.1, 0.1, 0.15, 0.1])
        self.radio_fractal = RadioButtons(
            ax_fractal_type, ('mandelbrot', 'julia'), active=0
        )
        self.radio_fractal.on_clicked(self.set_fractal_type)
        
        ax_colormap = plt.axes([0.35, 0.1, 0.25, 0.1])
        self.radio_colormap = RadioButtons(
            ax_colormap, self.available_colormaps, active=0
        )
        self.radio_colormap.on_clicked(self.set_colormap)
        
        ax_export = plt.axes([0.8, 0.1, 0.1, 0.05])
        self.button_export = Button(ax_export, 'Export to PNG')
        self.button_export.on_clicked(self.export_image)
        
        ax_c_real = plt.axes([0.65, 0.15, 0.1, 0.04])
        self.text_c_real = TextBox(
            ax_c_real, 'C real: ', initial=str(self.c_real)
        )
        self.text_c_real.on_submit(self.update_c_real)
        
        ax_c_imag = plt.axes([0.65, 0.1, 0.1, 0.04])
        self.text_c_imag = TextBox(
            ax_c_imag, 'C imaginary: ', initial=str(self.c_imag)
        )
        self.text_c_imag.on_submit(self.update_c_imag)
        
        ax_apply_c = plt.axes([0.8, 0.15, 0.1, 0.04])
        self.button_apply_c = Button(ax_apply_c, 'Aplikovat C')
        self.button_apply_c.on_clicked(self.apply_julia_c)
        

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        plt.show()
    
    def mandelbrot(self, h, w, max_iter):
        """calculates the Mandelbrot set."""
        y, x = np.ogrid[self.y_max:self.y_min:h*1j, self.x_min:self.x_max:w*1j]
        c = x + y*1j
        z = c.copy()
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def julia(self, h, w, max_iter):
        """Calculates the Julia set."""
        y, x = np.ogrid[self.y_max:self.y_min:h*1j, self.x_min:self.x_max:w*1j]
        z = x + y*1j
        c = self.c  # constant for Julia set
        divtime = max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2
        
        return divtime
    
    def create_fractal(self):
        """Creates and displays the fractal."""
        if hasattr(self, 'im') and self.im is not None:
            self.im.remove()
        
        # smaller resolution for zoomed in view
        # if the zoom is too small, we reduce the resolution to avoid performance issues
        if abs(self.x_max - self.x_min) < 0.01:
            current_resolution = int(self.resolution * 0.5)
        else:
            current_resolution = self.resolution
            
        if self.fractal_type == "mandelbrot":
            fractal = self.mandelbrot(current_resolution, current_resolution, self.max_iterations)
            title = f"Mandelbrot Set - Zoom: [{self.x_min:.4f}, {self.x_max:.4f}] × [{self.y_min:.4f}, {self.y_max:.4f}]"
        else:  # julia
            fractal = self.julia(current_resolution, current_resolution, self.max_iterations)
            title = f"Julia Set (c={self.c_real}+{self.c_imag}i) - Zoom: [{self.x_min:.4f}, {self.x_max:.4f}] × [{self.y_min:.4f}, {self.y_max:.4f}]"
        
        self.im = self.ax.imshow(
            fractal, cmap=self.colormap, 
            extent=[self.x_min, self.x_max, self.y_min, self.y_max]
        )
        
        self.ax.set_title(title)
        self.fig.canvas.draw_idle()
    
    def update_from_slider(self, val):
        """Updates the number of iterations from the slider."""
        self.max_iterations = int(self.slider_iterations.val)
        self.create_fractal()
    
    def update_c_real(self, text):
        """Updates real part of constant C."""
        try:
            self.c_real = float(text)
            # constant c is updated only after pressing the Apply button
        except ValueError:
            self.text_c_real.set_val(str(self.c_real))
    
    def update_c_imag(self, text):
        try:
            self.c_imag = float(text)
            # constant c is updated only after pressing the Apply button
        except ValueError:
            self.text_c_imag.set_val(str(self.c_imag))
    
    def apply_julia_c(self, event):
        self.c = complex(self.c_real, self.c_imag)
        if self.fractal_type == "julia":
            self.create_fractal()
    
    def reset_zoom(self, event):
        if self.fractal_type == "mandelbrot":
            self.x_min, self.x_max = -2.0, 1.0
            self.y_min, self.y_max = -1.5, 1.5
        else:  # julia
            self.x_min, self.x_max = -2.0, 2.0
            self.y_min, self.y_max = -2.0, 2.0
        
        self.create_fractal()
    
    def set_fractal_type(self, label):

        self.fractal_type = label
        # reseting zoom to default values for the selected fractal type
        self.reset_zoom(None)
    
    def set_colormap(self, label):
        self.colormap = label
        self.create_fractal()
    
    def export_image(self, event):
        if self.fractal_type == "mandelbrot":
            filename = f"mandelbrot_{self.x_min:.2f}_{self.x_max:.2f}_{self.y_min:.2f}_{self.y_max:.2f}.png"
        else:  # julia
            filename = f"julia_{self.c_real:.2f}_{self.c_imag:.2f}_{self.x_min:.2f}_{self.x_max:.2f}.png"
            
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Picture saved as: {filename}")
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        if event.button == 1:
            zoom_in = True
        elif event.button == 3:
            zoom_in = False
        else:
            return
        

        x, y = event.xdata, event.ydata
        
        # new boundaries for zoom
        current_width = self.x_max - self.x_min
        current_height = self.y_max - self.y_min
        
        if zoom_in:
            # zoom in
            new_width = current_width * self.zoom_factor
            new_height = current_height * self.zoom_factor
        else:
            # zoom out
            new_width = current_width / self.zoom_factor
            new_height = current_height / self.zoom_factor
        
        # New boundaries
        self.x_min = x - new_width / 2
        self.x_max = x + new_width / 2
        self.y_min = y - new_height / 2
        self.y_max = y + new_height / 2
        
        # recalculating the fractal with new boundaries
        self.create_fractal()

if __name__ == "__main__":
    FractalVisualizer()