import pygame
import numpy as np
import sys
from typing import Tuple

class HopfieldNetwork:
    def __init__(self, size: int):
        self.size = size
        self.total_units = size * size
        self.patterns = [] # ukládání patternů
        self.weights = np.zeros((self.total_units, self.total_units))
        
    def add_pattern(self, pattern: np.ndarray) -> None:
        # Převod na bipolar form (-1, 1)
        bipolar_pattern = 2 * pattern - 1
        
        # Reshape
        if bipolar_pattern.ndim > 1:
            bipolar_pattern = bipolar_pattern.flatten()
            
        # Uložení patternu
        self.patterns.append(bipolar_pattern)
        
        # Aktualizace vah
        pattern_matrix = np.outer(bipolar_pattern, bipolar_pattern)
        np.fill_diagonal(pattern_matrix, 0)  # No self-connections
        self.weights += pattern_matrix
        
    def get_weighted_matrix(self) -> np.ndarray:
        return self.weights
        
    def reconstruct_sync(self, pattern: np.ndarray, max_iterations: int = 10) -> np.ndarray:
        # Převod na bipolar form (-1, 1)
        bipolar_pattern = 2 * pattern - 1
        
        # Reshape
        if bipolar_pattern.ndim > 1:
            bipolar_pattern = bipolar_pattern.flatten()
            
        current_state = bipolar_pattern.copy()
        
        # Iterujeme dokud nedosáhneme max_iterations
        for _ in range(max_iterations):
            # Calculate new state (all units at once)
            new_state = np.sign(np.dot(self.weights, current_state))
            # Fix zeros (sign(0) = 0, but we want 1 or -1)
            new_state[new_state == 0] = 1
            
            # Check for convergence
            if np.array_equal(new_state, current_state):
                break
                
            current_state = new_state
        
        # Převod na binární tvar (0, 1)
        return (current_state + 1) / 2
        
    def reconstruct_async(self, pattern: np.ndarray, max_iterations: int = 50) -> np.ndarray:
        # Převod na bipolar form (-1, 1)
        bipolar_pattern = 2 * pattern - 1
        
        if bipolar_pattern.ndim > 1:
            bipolar_pattern = bipolar_pattern.flatten()
            
        current_state = bipolar_pattern.copy()
        
        # Iterujeme dokud nedosáhneme max_iterations
        for _ in range(max_iterations):
            # Aktualizujeme každou jednotku náhodně
            for i in range(self.total_units):
                idx = np.random.randint(0, self.total_units)
                activation = np.dot(self.weights[idx], current_state)
                current_state[idx] = 1 if activation >= 0 else -1
        
        # Převod na binární tvar (0, 1)
        return (current_state + 1) / 2
        
    def forget_pattern(self, pattern_idx: int) -> None:
        if 0 <= pattern_idx < len(self.patterns):
            del self.patterns[pattern_idx]
            
            # Znovu vypočítání vah
            self.weights = np.zeros((self.total_units, self.total_units))
            for pattern in self.patterns:
                pattern_matrix = np.outer(pattern, pattern)
                np.fill_diagonal(pattern_matrix, 0)
                self.weights += pattern_matrix

class HopfieldGUI:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (230, 230, 230)
    BLUE = (0, 120, 255)
    RED = (255, 100, 100)
    GREEN = (100, 200, 100)
    
    def __init__(self, grid_size: int = 5, cell_size: int = 80):
        pygame.init()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid_margin = 2
        self.button_height = 40
        self.button_margin = 10
        
        grid_width = grid_size * (cell_size + self.grid_margin) + self.grid_margin
        grid_height = grid_size * (cell_size + self.grid_margin) + self.grid_margin
        
        self.panel_width = 300
        
        window_width = grid_width + self.panel_width
        window_height = grid_height + 4 * (self.button_height + self.button_margin)
        
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Hopfield Network - 5x5 Grid")
        
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        
        self.network = HopfieldNetwork(grid_size)

        self.buttons = []
        button_width = (window_width - self.panel_width - 4 * self.button_margin) // 3
        
        y_pos = grid_height + self.button_margin
        self.buttons.append({
            'rect': pygame.Rect(self.button_margin, y_pos, button_width, self.button_height),
            'text': 'Save Pattern',
            'action': self.save_pattern
        })
        
        self.buttons.append({
            'rect': pygame.Rect(2 * self.button_margin + button_width, y_pos, button_width, self.button_height),
            'text': 'Sync',
            'action': self.reconstruct_sync
        })
        
        self.buttons.append({
            'rect': pygame.Rect(3 * self.button_margin + 2 * button_width, y_pos, button_width, self.button_height),
            'text': 'Async',
            'action': self.reconstruct_async
        })
        
        y_pos += self.button_height + self.button_margin
        self.buttons.append({
            'rect': pygame.Rect(self.button_margin, y_pos, button_width, self.button_height),
            'text': 'Show Patterns',
            'action': self.show_patterns
        })
        
        self.buttons.append({
            'rect': pygame.Rect(2 * self.button_margin + button_width, y_pos, button_width, self.button_height),
            'text': 'Clear Grid',
            'action': self.clear_grid
        })
        
        self.buttons.append({
            'rect': pygame.Rect(3 * self.button_margin + 2 * button_width, y_pos, button_width, self.button_height),
            'text': 'Weight Matrix',
            'action': self.show_weight_matrix
        })
        
        self.font = pygame.font.SysFont(None, 24)
        
        self.showing_patterns = False
        self.showing_weight_matrix = False
        self.show_vectors = False
        self.current_pattern_page = 0
        self.patterns_per_page = 3
        
        self.nav_buttons = []
        
        self.clock = pygame.time.Clock()
        
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                    
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_buttons()
            
            if self.showing_patterns:
                self.draw_patterns()
            elif self.showing_weight_matrix:
                self.draw_weight_matrix()
                
            pygame.display.flip()
            self.clock.tick(30)
            
        pygame.quit()
        sys.exit()
        
    def handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        
        grid_width = self.grid_size * (self.cell_size + self.grid_margin) + self.grid_margin
        grid_height = self.grid_size * (self.cell_size + self.grid_margin) + self.grid_margin
        
        if x < grid_width and y < grid_height:
            col = x // (self.cell_size + self.grid_margin)
            row = y // (self.cell_size + self.grid_margin)
            
            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                self.grid[row][col] = 1 - self.grid[row][col]
                
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                button['action']()
                return
                
        for button in self.nav_buttons:
            if button['rect'].collidepoint(pos):
                button['action']()
                return
                
        if self.showing_patterns:
            self.handle_pattern_display_click(pos)
            
    def handle_pattern_display_click(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        
        option_y = 50
        option_x = self.grid_size * (self.cell_size + self.grid_margin) + self.grid_margin + 20
        
        toggle_rect = pygame.Rect(option_x, option_y, 150, 30)
        if toggle_rect.collidepoint(pos):
            self.show_vectors = not self.show_vectors
            return
            
        start_idx = self.current_pattern_page * self.patterns_per_page
        end_idx = min(start_idx + self.patterns_per_page, len(self.network.patterns))
        
        for i in range(start_idx, end_idx):
            rel_idx = i - start_idx
            forget_button_y = 120 + rel_idx * 110
            forget_button_rect = pygame.Rect(option_x + 180, forget_button_y, 80, 30)
            
            if forget_button_rect.collidepoint(pos):
                self.network.forget_pattern(i)
                if len(self.network.patterns) <= start_idx and self.current_pattern_page > 0:
                    self.current_pattern_page -= 1
                return
        
    def draw_grid(self) -> None:
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * (self.cell_size + self.grid_margin) + self.grid_margin
                y = row * (self.cell_size + self.grid_margin) + self.grid_margin
                
                color = self.BLACK if self.grid[row][col] == 1 else self.WHITE
                pygame.draw.rect(self.screen, color, [x, y, self.cell_size, self.cell_size])
                
                pygame.draw.rect(self.screen, self.GRAY, [x, y, self.cell_size, self.cell_size], 1)
    
    def draw_buttons(self) -> None:
        for button in self.buttons:
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, button['rect'])
            
            pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
            
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
            
        for button in self.nav_buttons:
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, button['rect'])
            pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
    
    def save_pattern(self) -> None:
        if np.any(self.grid):
            self.network.add_pattern(self.grid.copy())
            print("Pattern saved!")
            
            self.showing_patterns = False
            self.showing_weight_matrix = False
    
    def reconstruct_sync(self) -> None:
        if len(self.network.patterns) > 0:
            result = self.network.reconstruct_sync(self.grid)
            self.grid = result.reshape(self.grid_size, self.grid_size)
            print("Synchronous reconstruction completed!")
            
            self.showing_patterns = False
            self.showing_weight_matrix = False
    
    def reconstruct_async(self) -> None:
        if len(self.network.patterns) > 0:
            result = self.network.reconstruct_async(self.grid)
            self.grid = result.reshape(self.grid_size, self.grid_size)
            print("Asynchronous reconstruction completed!")
            
            self.showing_patterns = False
            self.showing_weight_matrix = False
    
    def show_patterns(self) -> None:
        for pattern in self.network.patterns:
            print("-" * 20)
            print(pattern)
            print("-" * 20)
        self.showing_patterns = True
        self.showing_weight_matrix = False
        self.current_pattern_page = 0
        
        # Create navigation buttons
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self) -> None:
        self.nav_buttons = []
        
        if len(self.network.patterns) > self.patterns_per_page:
            panel_x = self.grid_size * (self.cell_size + self.grid_margin) + self.grid_margin + 20
            button_y = 400
            button_width = 80
            
            if self.current_pattern_page > 0:
                self.nav_buttons.append({
                    'rect': pygame.Rect(panel_x, button_y, button_width, 30),
                    'text': 'Previous',
                    'action': self.prev_pattern_page
                })
            
            if (self.current_pattern_page + 1) * self.patterns_per_page < len(self.network.patterns):
                self.nav_buttons.append({
                    'rect': pygame.Rect(panel_x + 100, button_y, button_width, 30),
                    'text': 'Next',
                    'action': self.next_pattern_page
                })
    
    def prev_pattern_page(self) -> None:
        if self.current_pattern_page > 0:
            self.current_pattern_page -= 1
            self.update_navigation_buttons()
    
    def next_pattern_page(self) -> None:
        if (self.current_pattern_page + 1) * self.patterns_per_page < len(self.network.patterns):
            self.current_pattern_page += 1
            self.update_navigation_buttons()
    
    def clear_grid(self) -> None:
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        self.showing_patterns = False
        self.showing_weight_matrix = False
    
    def show_weight_matrix(self) -> None:
        self.showing_weight_matrix = True
        self.showing_patterns = False
    
    def draw_patterns(self) -> None:
        if len(self.network.patterns) == 0:
            text = self.font.render("No patterns saved", True, self.BLACK)
            self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, 50))
            return
            
        text = self.font.render("Saved Patterns:", True, self.BLACK)
        self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, 20))
        
        option_text = "Show as: " + ("Vector" if self.show_vectors else "Matrix")
        text = self.font.render(option_text, True, self.BLUE)
        text_rect = text.get_rect()
        text_rect.topleft = (self.grid_size * (self.cell_size + self.grid_margin) + 20, 50)
        self.screen.blit(text, text_rect)
        
        pygame.draw.rect(self.screen, self.BLUE, 
                         (text_rect.left, text_rect.top, text_rect.width, text_rect.height), 1)
        
        start_idx = self.current_pattern_page * self.patterns_per_page
        end_idx = min(start_idx + self.patterns_per_page, len(self.network.patterns))
        
        for i in range(start_idx, end_idx):
            pattern = self.network.patterns[i]
            # Převod z bipolar na binární formu pro zobrazení
            binary_pattern = (pattern + 1) / 2
            
            y_offset = 120 + (i - start_idx) * 110
            
            text = self.font.render(f"Pattern {i+1}:", True, self.BLACK)
            self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, y_offset))
            
            forget_btn_rect = pygame.Rect(
                self.grid_size * (self.cell_size + self.grid_margin) + 200, 
                y_offset, 
                80, 30
            )
            pygame.draw.rect(self.screen, self.RED, forget_btn_rect)
            text = self.font.render("Forget", True, self.WHITE)
            text_rect = text.get_rect(center=forget_btn_rect.center)
            self.screen.blit(text, text_rect)
            
            if self.show_vectors:
                # Zobrazení patternu jako vektor
                vector_text = ' '.join([str(int(val)) for val in binary_pattern])
                text = self.font.render(vector_text, True, self.BLACK)
                self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, y_offset + 30))
            else:
                # Zobrazení patternu jako matice
                pattern_2d = binary_pattern.reshape(self.grid_size, self.grid_size)
                cell_size = 20
                for row in range(self.grid_size):
                    for col in range(self.grid_size):
                        x = self.grid_size * (self.cell_size + self.grid_margin) + 20 + col * (cell_size + 1)
                        y = y_offset + 30 + row * (cell_size + 1)
                        
                        color = self.BLACK if pattern_2d[row][col] == 1 else self.WHITE
                        pygame.draw.rect(self.screen, color, [x, y, cell_size, cell_size])
                        pygame.draw.rect(self.screen, self.GRAY, [x, y, cell_size, cell_size], 1)
    
    def draw_weight_matrix(self) -> None:
        if len(self.network.patterns) == 0:
            text = self.font.render("No patterns saved - no weights", True, self.BLACK)
            self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, 50))
            return
            
        text = self.font.render("Weight Matrix:", True, self.BLACK)
        self.screen.blit(text, (self.grid_size * (self.cell_size + self.grid_margin) + 20, 20))
        
        weights = self.network.get_weighted_matrix()
        
        min_weight = np.min(weights)
        max_weight = np.max(weights)
        weight_range = max(abs(min_weight), abs(max_weight))
        
        if weight_range == 0:
            weight_range = 1  # dělení nulou
        
        cell_size = min(15, self.panel_width // (self.total_units + 2))
        for i in range(self.total_units):
            for j in range(self.total_units):
                x = self.grid_size * (self.cell_size + self.grid_margin) + 20 + j * (cell_size + 1)
                y = 50 + i * (cell_size + 1)
                
                weight = weights[i][j]
                if weight > 0:
                    intensity = int(255 * (weight / weight_range))
                    color = (255 - intensity, 255 - intensity, 255)
                else:
                    intensity = int(255 * (abs(weight) / weight_range))
                    color = (255, 255 - intensity, 255 - intensity)
                
                pygame.draw.rect(self.screen, color, [x, y, cell_size, cell_size])
                pygame.draw.rect(self.screen, self.GRAY, [x, y, cell_size, cell_size], 1)
        
        scale_x = self.grid_size * (self.cell_size + self.grid_margin) + 20
        scale_y = 50 + (self.total_units + 2) * (cell_size + 1)
        scale_width = 200
        scale_height = 20
        
        for i in range(scale_width):
            val = 2 * (i / scale_width) - 1
            if val > 0:
                intensity = int(255 * val)
                color = (255 - intensity, 255 - intensity, 255)
            else:
                intensity = int(255 * abs(val))
                color = (255, 255 - intensity, 255 - intensity)
                
            pygame.draw.rect(self.screen, color, [scale_x + i, scale_y, 1, scale_height])
        
        pygame.draw.rect(self.screen, self.BLACK, [scale_x, scale_y, scale_width, scale_height], 1)
        neg_text = self.font.render(f"{min_weight:.2f}", True, self.BLACK)
        self.screen.blit(neg_text, (scale_x, scale_y + scale_height + 5))
        pos_text = self.font.render(f"{max_weight:.2f}", True, self.BLACK)
        pos_rect = pos_text.get_rect()
        self.screen.blit(pos_text, (scale_x + scale_width - pos_rect.width, scale_y + scale_height + 5))
        zero_text = self.font.render("0", True, self.BLACK)
        zero_rect = zero_text.get_rect()
        self.screen.blit(zero_text, (scale_x + scale_width//2 - zero_rect.width//2, scale_y + scale_height + 5))

    @property
    def total_units(self) -> int:
        return self.grid_size ** 2

def main():
    app = HopfieldGUI(grid_size=5, cell_size=80)
    app.run()

if __name__ == "__main__":
    main()
