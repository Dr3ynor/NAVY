import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

class ForestFireCA:
    # Cell states
    EMPTY = 0
    TREE = 1
    BURNING = 2
    BURNT = 3
    
    def __init__(self, width=100, height=100, p=0.05, f=0.001, forest_density=0.5, neighborhood='von_neumann', burnout_prob=1.0, regrow_prob=0.3):
        self.width = width
        self.height = height
        self.p = p  # Probability of tree growth
        self.f = f  # Probability of spontaneous fire
        self.forest_density = forest_density  # Initial forest density
        self.neighborhood = neighborhood  # 'von_neumann' or 'moore'
        self.burnout_prob = burnout_prob  # Probability a burning tree burns out
        self.regrow_prob = regrow_prob  # Probability a burnt tree can start regrowing
        
        # Initialize grid
        self.grid = np.zeros((height, width), dtype=int)
        self.initialize_forest()
    
    def initialize_forest(self):
        # Create a random forest with the given density
        random_grid = np.random.random((self.height, self.width))
        self.grid = np.where(random_grid < self.forest_density, self.TREE, self.EMPTY)
        
    def get_neighbors(self, i, j):
        neighbors = []
        
        if self.neighborhood == 'von_neumann':
            # Von Neumann neighborhood (4 adjacent cells: up, right, down, left)
            if i > 0:
                neighbors.append((i-1, j))
            if i < self.height - 1:
                neighbors.append((i+1, j))
            if j > 0:
                neighbors.append((i, j-1))
            if j < self.width - 1:
                neighbors.append((i, j+1))
                
        elif self.neighborhood == 'moore':
            # Moore neighborhood (8 surrounding cells, including diagonals)
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:  # Skip the cell itself
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbors.append((ni, nj))
        
        return neighbors
    
    def update(self):
        new_grid = np.copy(self.grid)
        
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i, j] == self.EMPTY:
                    # An empty cell can grow a tree with probability p
                    if np.random.random() < self.p:
                        new_grid[i, j] = self.TREE
                
                elif self.grid[i, j] == self.TREE:
                    # Check if any neighbor is burning
                    neighbors = self.get_neighbors(i, j)
                    neighbor_burning = False
                    
                    for ni, nj in neighbors:
                        if self.grid[ni, nj] == self.BURNING:
                            neighbor_burning = True
                            break
                    
                    if neighbor_burning:
                        # Tree catches fire if neighbor is burning
                        new_grid[i, j] = self.BURNING
                    elif np.random.random() < self.f:
                        # Tree spontaneously catches fire with probability f
                        new_grid[i, j] = self.BURNING
                
                elif self.grid[i, j] == self.BURNING:
                    # A burning tree burns out with burnout_prob
                    if np.random.random() < self.burnout_prob:
                        new_grid[i, j] = self.BURNT
                
                elif self.grid[i, j] == self.BURNT:
                    # A burnt tree can start regrowing (become empty) with regrow_prob
                    if np.random.random() < self.regrow_prob:
                        new_grid[i, j] = self.EMPTY
        
        self.grid = new_grid
        return self.grid

# Set up the simulation and visualization
def main():
    # Simulation parameters
    width, height = 100, 100
    p_initial = 0.05  # Tree growth probability
    f_initial = 0.001  # Spontaneous fire probability
    forest_density_initial = 0.5  # Initial forest density
    burnout_prob_initial = 1.0  # Probability a burning tree burns out
    regrow_prob_initial = 0.3  # Probability a burnt tree can start regrowing
    
    # Create the forest fire model
    ca = ForestFireCA(width, height, p_initial, f_initial, forest_density_initial)
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.95)
    
    # Create custom colormap
    colors = ['black', 'green', 'red', 'gray']  # empty, tree, burning, burnt
    cmap = mcolors.ListedColormap(colors)
    bounds = [0, 1, 2, 3, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    # Initialize the plot
    img = ax.imshow(ca.grid, cmap=cmap, norm=norm, animated=True)
    ax.set_title('Forest Fire Cellular Automaton')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add color bar
    cbar = plt.colorbar(img, ticks=[0.5, 1.5, 2.5, 3.5])
    cbar.set_ticklabels(['Empty', 'Tree', 'Burning', 'Burnt'])
    
    # Add sliders
    ax_p = plt.axes([0.1, 0.20, 0.65, 0.03])
    p_slider = Slider(ax_p, 'Growth Probability (p)', 0.0, 0.2, valinit=p_initial, valstep=0.001)
    
    ax_f = plt.axes([0.1, 0.15, 0.65, 0.03])
    f_slider = Slider(ax_f, 'Ignition Probability (f)', 0.0, 0.01, valinit=f_initial, valstep=0.0001)
    
    ax_density = plt.axes([0.1, 0.10, 0.65, 0.03])
    density_slider = Slider(ax_density, 'Initial Forest Density', 0.1, 1.0, valinit=forest_density_initial, valstep=0.05)
    
    ax_burnout = plt.axes([0.1, 0.05, 0.30, 0.03])
    burnout_slider = Slider(ax_burnout, 'Burnout Probability', 0.1, 1.0, valinit=burnout_prob_initial, valstep=0.05)
    
    ax_regrow = plt.axes([0.45, 0.05, 0.30, 0.03])
    regrow_slider = Slider(ax_regrow, 'Regrow Probability', 0.0, 1.0, valinit=regrow_prob_initial, valstep=0.05)
    
    # Add radio buttons for neighborhood selection
    ax_radio = plt.axes([0.8, 0.1, 0.15, 0.15])
    radio = RadioButtons(ax_radio, ('von_neumann', 'moore'), active=0)
    
    # Add reset button
    ax_reset = plt.axes([0.8, 0.05, 0.15, 0.03])
    reset_button = Button(ax_reset, 'Reset')
    
    # Update function for the animation
    def update(frame):
        ca.update()
        img.set_array(ca.grid)
        return [img]
    
    # Reset function
    def reset(event):
        ca.p = p_slider.val
        ca.f = f_slider.val
        ca.forest_density = density_slider.val
        ca.burnout_prob = burnout_slider.val
        ca.regrow_prob = regrow_slider.val
        ca.initialize_forest()
        img.set_array(ca.grid)
        fig.canvas.draw_idle()
    
    # Update parameters when sliders change
    def update_p(val):
        ca.p = val
    
    def update_f(val):
        ca.f = val
    
    def update_density(val):
        ca.forest_density = val
    
    def update_burnout(val):
        ca.burnout_prob = val
    
    def update_regrow(val):
        ca.regrow_prob = val
    
    def update_neighborhood(label):
        ca.neighborhood = label
    
    # Connect the update functions to the widgets
    p_slider.on_changed(update_p)
    f_slider.on_changed(update_f)
    density_slider.on_changed(update_density)
    burnout_slider.on_changed(update_burnout)
    regrow_slider.on_changed(update_regrow)
    radio.on_clicked(update_neighborhood)
    reset_button.on_clicked(reset)
    
    # Create the animation
    ani = FuncAnimation(fig, update, frames=None, interval=50, blit=True)
    
    plt.show()

if __name__ == "__main__":
    main()