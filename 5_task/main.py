import tkinter as tk
from tkinter import ttk, StringVar, DoubleVar, IntVar
from math import sin, cos, radians, pi
import colorsys

class LSystemFractal:
    def __init__(self, axiom="F", rules=None, angle=90, line_length=10, start_x=0, start_y=0, start_angle=0):
        self.axiom = axiom
        self.rules = rules or {"F": "F+F-F-FF+F+F-F"}
        self.angle = angle
        self.line_length = line_length
        self.start_x = start_x
        self.start_y = start_y
        self.start_angle = start_angle
        self.current_string = axiom
        
    def generate(self, iterations):
        result = self.axiom
        for _ in range(iterations):
            next_result = ""
            for char in result:
                next_result += self.rules.get(char, char)
            result = next_result
        self.current_string = result
        return result
    
    def get_bounds(self):
        """Calculate the bounds of the fractal to assist with scaling"""
        x, y = self.start_x, self.start_y
        angle = radians(self.start_angle)
        min_x, max_x = x, x
        min_y, max_y = y, y
        stack = []
        
        for char in self.current_string:
            if char == 'F':
                x += self.line_length * cos(angle)
                y += self.line_length * sin(angle)
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
            elif char == 'b':
                x += self.line_length * cos(angle)
                y += self.line_length * sin(angle)
            elif char == '+':
                angle += radians(self.angle)
            elif char == '-':
                angle -= radians(self.angle)
            elif char == '[':
                stack.append((x, y, angle))
            elif char == ']':
                if stack:
                    x, y, angle = stack.pop()
        
        return min_x, min_y, max_x, max_y
        
    def draw(self, canvas, zoom=1.0, x_offset=0, y_offset=0, color_mode=False):
        canvas.delete("all")
        
        # Calculate starting position based on zoom and offsets
        x = self.start_x * zoom - x_offset
        y = self.start_y * zoom - y_offset
        angle = radians(self.start_angle)
        stack = []
        
        line_length = self.line_length * zoom
        
        # For color gradient based on depth
        depth = 0
        max_depth = 0
        for char in self.current_string:
            if char == '[':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ']':
                depth -= 1
        
        # Draw the L-system
        depth = 0
        for i, char in enumerate(self.current_string):
            if char == 'F':
                old_x, old_y = x, y
                x += line_length * cos(angle)
                y += line_length * sin(angle)
                
                if color_mode:
                    # Create color gradient based on position in string
                    hue = i / len(self.current_string)
                    rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                    color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
                else:
                    color = "#FFFFFF"  # White
                
                canvas.create_line(old_x, old_y, x, y, fill=color, width=1)
            elif char == 'b':
                x += line_length * cos(angle)
                y += line_length * sin(angle)
            elif char == '+':
                angle += radians(self.angle)
            elif char == '-':
                angle -= radians(self.angle)
            elif char == '[':
                stack.append((x, y, angle))
                depth += 1
            elif char == ']':
                if stack:
                    x, y, angle = stack.pop()
                    depth -= 1

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("L-System Fractal Generator")
        self.root.geometry("1200x800")
        self.setup_styles()
        
        self.predefined_systems = {
            "Koch Snowflake": {
                "axiom": "F+F+F+F",
                "rule": "F -> F+F-F-FF+F+F-F",
                "angle": 90
            },
            "Koch Curve": {
                "axiom": "F++F++F",
                "rule": "F -> F+F--F+F",
                "angle": 60
            },
            "Plant": {
                "axiom": "F",
                "rule": "F -> F[+F]F[-F]F",
                "angle": 180 * (pi/7) / pi  # Converting radians to degrees
            },
            "Bush": {
                "axiom": "F",
                "rule": "F -> FF+[+F-F-F]-[-F+F+F]",
                "angle": 180 * (pi/8) / pi  # Converting radians to degrees
            }
        }



        # Variables
        self.axiom_var = StringVar(value="F+F+F+F")
        self.rule_var = StringVar(value="F -> F+F-F-FF+F+F-F")
        self.angle_var = DoubleVar(value=90)
        self.iterations_var = IntVar(value=2)
        self.line_length_var = IntVar(value=5)
        self.start_x_var = IntVar(value=600)
        self.start_y_var = IntVar(value=400)
        self.start_angle_var = IntVar(value=0)
        
        # Zooming and panning
        self.zoom = 1.0
        self.x_offset = 0
        self.y_offset = 0
        self.dragging = False
        self.last_x = 0
        self.last_y = 0
        self.color_mode = False
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame, padding=10)
        controls_frame.pack(side="left", fill="y")
        
        # Canvas frame
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side="right", fill="both", expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="#1e1e1e", width=900, height=700)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Controls
        self.create_controls(controls_frame)
        
        # Predefined L-systems

        
        # Initialize fractal
        self.l_system = LSystemFractal(
            axiom=self.axiom_var.get(),
            rules=self.parse_rule(self.rule_var.get()),
            angle=self.angle_var.get(),
            line_length=self.line_length_var.get(),
            start_x=self.start_x_var.get(),
            start_y=self.start_y_var.get(),
            start_angle=self.start_angle_var.get()
        )
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.dragging_motion)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<MouseWheel>", self.zoom_wheel)  # Windows
        self.canvas.bind("<Button-4>", self.zoom_in)  # Linux
        self.canvas.bind("<Button-5>", self.zoom_out)  # Linux
        
        # Generate initial fractal
        self.redraw()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure colors for a dark theme
        style.configure("TFrame", background="#2d2d2d")
        style.configure("TLabel", background="#2d2d2d", foreground="#ffffff")
        style.configure("TButton", background="#3d3d3d", foreground="#ffffff")
        style.configure("TRadiobutton", background="#2d2d2d", foreground="#ffffff")
        style.configure("TCheckbutton", background="#2d2d2d", foreground="#ffffff")
        style.configure("TEntry", fieldbackground="#3d3d3d", foreground="#ffffff")
        style.configure("TCombobox", fieldbackground="#3d3d3d", foreground="#ffffff")
        
        # Set the window background
        self.root.configure(bg="#2d2d2d")
    
    def create_controls(self, parent):
        ttk.Label(parent, text="Predefined Fractals:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Predefined fractals combobox
        self.fractal_combo = ttk.Combobox(parent, values=list(self.predefined_systems.keys()), width=20)
        self.fractal_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.fractal_combo.bind("<<ComboboxSelected>>", self.load_predefined)
        
        # Parameters
        ttk.Label(parent, text="Axiom:").grid(row=2, column=0, sticky="w")
        axiom_entry = ttk.Entry(parent, textvariable=self.axiom_var, width=25)
        axiom_entry.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Rule (F -> ...):").grid(row=4, column=0, sticky="w")
        rule_entry = ttk.Entry(parent, textvariable=self.rule_var, width=25)
        rule_entry.grid(row=5, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Angle (degrees):").grid(row=6, column=0, sticky="w")
        angle_entry = ttk.Entry(parent, textvariable=self.angle_var, width=25)
        angle_entry.grid(row=7, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Angle (degrees):").grid(row=6, column=0, sticky="w")
        angle_entry = ttk.Entry(parent, textvariable=self.angle_var, width=25)
        angle_entry.grid(row=7, column=0, sticky="ew", pady=(0, 5))

        ttk.Label(parent, text="Iterations:").grid(row=8, column=0, sticky="w")
        iterations_entry = ttk.Entry(parent, textvariable=self.iterations_var, width=25)
        iterations_entry.grid(row=9, column=0, sticky="ew", pady=(0, 5))

        ttk.Label(parent, text="Line Length:").grid(row=10, column=0, sticky="w")
        length_entry = ttk.Entry(parent, textvariable=self.line_length_var, width=25)
        length_entry.grid(row=11, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Start Position X:").grid(row=12, column=0, sticky="w")
        start_x_entry = ttk.Entry(parent, textvariable=self.start_x_var, width=25)
        start_x_entry.grid(row=13, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Start Position Y:").grid(row=14, column=0, sticky="w")
        start_y_entry = ttk.Entry(parent, textvariable=self.start_y_var, width=25)
        start_y_entry.grid(row=15, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(parent, text="Start Angle:").grid(row=16, column=0, sticky="w")
        start_angle_entry = ttk.Entry(parent, textvariable=self.start_angle_var, width=25)
        start_angle_entry.grid(row=17, column=0, sticky="ew", pady=(0, 10))
        
        # Color mode
        self.color_var = tk.BooleanVar(value=False)
        color_check = ttk.Checkbutton(parent, text="Color Mode", variable=self.color_var, command=self.toggle_color)
        color_check.grid(row=18, column=0, sticky="w", pady=(0, 10))
        
        # Generate button
        generate_btn = ttk.Button(parent, text="Generate Fractal", command=self.redraw)
        generate_btn.grid(row=19, column=0, sticky="ew", pady=10)
        
        # Reset zoom/position button
        reset_btn = ttk.Button(parent, text="Reset View", command=self.reset_view)
        reset_btn.grid(row=20, column=0, sticky="ew")
        
        # Help text
        help_text = "L-System Controls:\nF = Draw forward\nb = Move forward (no line)\n+ = Turn right\n- = Turn left\n[ = Save position\n] = Restore position"
        help_label = ttk.Label(parent, text=help_text, justify="left", wraplength=200)
        help_label.grid(row=21, column=0, sticky="w", pady=(20, 0))
    
    def parse_rule(self, rule_text):
        try:
            parts = rule_text.split("->")
            symbol = parts[0].strip()
            replacement = parts[1].strip()
            return {symbol: replacement}
        except:
            return {"F": rule_text.strip()}
    
    def load_predefined(self, event):
        selected = self.fractal_combo.get()
        if selected in self.predefined_systems:
            system = self.predefined_systems[selected]
            self.axiom_var.set(system["axiom"])
            self.rule_var.set(f"F -> {system['rule'].split('->')[1].strip()}" 
                              if "->" in system["rule"] else f"F -> {system['rule']}")
            self.angle_var.set(system["angle"])
            self.reset_view()
            self.redraw()
    
    def toggle_color(self):
        self.color_mode = self.color_var.get()
        self.redraw()
    
    def redraw(self):
        # Update L-system parameters
        self.l_system = LSystemFractal(
            axiom=self.axiom_var.get(),
            rules=self.parse_rule(self.rule_var.get()),
            angle=self.angle_var.get(),
            line_length=self.line_length_var.get(),
            start_x=self.start_x_var.get(),
            start_y=self.start_y_var.get(),
            start_angle=self.start_angle_var.get()
        )
        
        # Generate the L-system string
        self.l_system.generate(self.iterations_var.get())
        
        # Draw the L-system
        self.l_system.draw(self.canvas, self.zoom, self.x_offset, self.y_offset, self.color_mode)
    
    def start_drag(self, event):
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y
    
    def dragging_motion(self, event):
        if not self.dragging:
            return
        
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        self.x_offset -= dx
        self.y_offset -= dy
        
        self.last_x = event.x
        self.last_y = event.y
        
        self.redraw()
    
    def stop_drag(self, event):
        self.dragging = False
    
    def zoom_wheel(self, event):
        """Handle mousewheel zoom on Windows"""
        delta = event.delta
        if delta > 0:
            self.zoom_in(event)
        else:
            self.zoom_out(event)
    
    def zoom_in(self, event):
        """Zoom in - ensure we zoom around the mouse position"""
        old_zoom = self.zoom
        self.zoom *= 1.2
        
        # Adjust offset to zoom around mouse position
        self.x_offset = event.x + (self.x_offset - event.x) * (self.zoom / old_zoom)
        self.y_offset = event.y + (self.y_offset - event.y) * (self.zoom / old_zoom)
        
        self.redraw()
        return "break"  # Prevent event propagation
    
    def zoom_out(self, event):
        """Zoom out - ensure we zoom around the mouse position"""
        if self.zoom <= 0.1:
            return "break"
        
        old_zoom = self.zoom
        self.zoom /= 1.2
        
        # Adjust offset to zoom around mouse position
        self.x_offset = event.x + (self.x_offset - event.x) * (self.zoom / old_zoom)
        self.y_offset = event.y + (self.y_offset - event.y) * (self.zoom / old_zoom)
        
        self.redraw()
        return "break"  # Prevent event propagation
    
    def reset_view(self):
        """Reset zoom and position"""
        self.zoom = 1.0
        self.x_offset = 0
        self.y_offset = 0
        self.redraw()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
