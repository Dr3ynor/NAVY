import pygame
import math
import sys
from collections import deque

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("L-System Generator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 100, 200)
RED = (200, 50, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 200, 0)

# Font setup
font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 24, bold=True)

# Predefined L-Systems
l_systems = [
    {
        "name": "System 1 - Square Filling Curve",
        "axiom": "F+F+F+F",
        "rules": {"F": "F+F-F-FF+F+F-F"},
        "angle": 90,
        "initial_angle": 0,
        "length": 5,
        "color": GREEN
    },
    {
        "name": "System 2 - Koch Snowflake Variation",
        "axiom": "F++F++F",
        "rules": {"F": "F+F--F+F"},
        "angle": 60,
        "initial_angle": 0,
        "length": 5,
        "color": BLUE
    },
    {
        "name": "System 3 - Plant Structure",
        "axiom": "F",
        "rules": {"F": "F[+F]F[-F]F"},
        "angle": math.pi/7 * 180/math.pi,  # Convert radians to degrees
        "initial_angle": -90,  # Start growing upward
        "length": 5,
        "color": GREEN
    },
    {
        "name": "System 4 - Branching Tree",
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": math.pi/8 * 180/math.pi,  # Convert radians to degrees
        "initial_angle": -90,  # Start growing upward
        "length": 5,
        "color": RED
    }
]

# UI state
current_system = 0
iterations = 3
auto_center = True
drawing = False  # Flag to track if we're currently drawing
show_help = False

# Initialize the fractal string based on the default selection
fractal_string = l_systems[current_system]["axiom"]

def generate_l_system(axiom, rules, iterations):
    """Generate the L-system string based on axiom, rules and iterations"""
    result = axiom
    for _ in range(iterations):
        new_result = ""
        for char in result:
            if char in rules:
                new_result += rules[char]
            else:
                new_result += char
        result = new_result
    return result

def draw_l_system(string, angle_deg, initial_angle, length, color):
    """Draw the L-system based on the generated string"""
    global drawing
    drawing = True
    
    # Convert degrees to radians
    angle_rad = math.radians(angle_deg)
    current_angle = math.radians(initial_angle)
    
    # Calculate bounds to center the fractal
    if auto_center:
        min_x, max_x, min_y, max_y = calculate_bounds(string, angle_rad, current_angle, length)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Scale factor to fit in screen (with margin)
        width_scale = (WIDTH - 300) * 0.8 / max(1, max_x - min_x)
        height_scale = HEIGHT * 0.8 / max(1, max_y - min_y)
        scale = min(width_scale, height_scale)
        
        # Don't scale up too much for small fractals
        scale = min(scale, 10)
        
        # Adjusted length
        adjusted_length = length * scale
        
        # Starting position (centered)
        pos_x = WIDTH/2 - center_x * scale
        pos_y = HEIGHT/2 - center_y * scale
    else:
        # Default starting position when auto-center is off
        adjusted_length = length
        pos_x, pos_y = WIDTH / 2, HEIGHT / 2
    
    # Stack for storing positions and angles
    stack = deque()
    
    # Draw the fractal
    for char in string:
        if char == 'F':
            # Calculate new position
            new_x = pos_x + adjusted_length * math.cos(current_angle)
            new_y = pos_y + adjusted_length * math.sin(current_angle)
            
            # Draw line
            pygame.draw.line(screen, color, (pos_x, pos_y), (new_x, new_y), 1)
            
            # Update position
            pos_x, pos_y = new_x, new_y
            
            # Update screen occasionally for smoother visual
            if len(string) < 10000 or pygame.time.get_ticks() % 100 == 0:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
        elif char == 'b':
            # Move without drawing
            pos_x += adjusted_length * math.cos(current_angle)
            pos_y += adjusted_length * math.sin(current_angle)
        
        elif char == '+':
            # Turn right
            current_angle += angle_rad
        
        elif char == '-':
            # Turn left
            current_angle -= angle_rad
        
        elif char == '[':
            # Save current position and angle
            stack.append((pos_x, pos_y, current_angle))
        
        elif char == ']':
            # Restore position and angle
            if stack:
                pos_x, pos_y, current_angle = stack.pop()
    
    drawing = False

def calculate_bounds(string, angle_rad, initial_angle, length=1):
    """Calculate the bounds of the L-system for centering purposes"""
    current_angle = initial_angle
    x, y = 0, 0
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    
    # Stack for storing positions and angles
    stack = deque()
    
    for char in string:
        if char == 'F' or char == 'b':
            # Calculate new position
            new_x = x + length * math.cos(current_angle)
            new_y = y + length * math.sin(current_angle)
            
            # Update bounds
            min_x = min(min_x, new_x)
            max_x = max(max_x, new_x)
            min_y = min(min_y, new_y)
            max_y = max(max_y, new_y)
            
            # Update position
            x, y = new_x, new_y
        
        elif char == '+':
            # Turn right
            current_angle += angle_rad
        
        elif char == '-':
            # Turn left
            current_angle -= angle_rad
        
        elif char == '[':
            # Save current position and angle
            stack.append((x, y, current_angle))
        
        elif char == ']':
            # Restore position and angle
            if stack:
                x, y, current_angle = stack.pop()
    
    return min_x, max_x, min_y, max_y

def draw_ui():
    """Draw the user interface elements"""
    # Draw sidebar
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, 280, HEIGHT))
    
    # Title
    title = title_font.render("L-System Generator", True, WHITE)
    screen.blit(title, (20, 20))
    
    # Current system info
    system_info = font.render("System: " + l_systems[current_system]["name"], True, WHITE)
    screen.blit(system_info, (20, 60))
    
    # Iterations
    iter_info = font.render(f"Iterations: {iterations}", True, WHITE)
    screen.blit(iter_info, (20, 90))
    
    # Axiom
    axiom_info = font.render(f"Axiom: {l_systems[current_system]['axiom']}", True, WHITE)
    screen.blit(axiom_info, (20, 120))
    
    # Rules (may need to wrap for long rules)
    rule_text = f"Rule: F → {l_systems[current_system]['rules']['F']}"
    if len(rule_text) > 36:
        rule_text = rule_text[:36] + "..."
    rule_info = font.render(rule_text, True, WHITE)
    screen.blit(rule_info, (20, 150))
    
    # Angle
    angle_info = font.render(f"Angle: {l_systems[current_system]['angle']}°", True, WHITE)
    screen.blit(angle_info, (20, 180))
    
    # Draw buttons
    buttons = [
        {"text": "Generate", "y": 220, "color": GREEN},
        {"text": "Previous System", "y": 260, "color": BLUE},
        {"text": "Next System", "y": 300, "color": BLUE},
        {"text": "Decrease Iterations", "y": 340, "color": YELLOW},
        {"text": "Increase Iterations", "y": 380, "color": YELLOW},
        {"text": f"Auto Center: {'ON' if auto_center else 'OFF'}", "y": 420, "color": GRAY},
        {"text": "Show Help", "y": 460, "color": WHITE},
    ]
    
    for button in buttons:
        pygame.draw.rect(screen, button["color"], (20, button["y"], 240, 30))
        btn_text = font.render(button["text"], True, BLACK)
        screen.blit(btn_text, (30, button["y"] + 5))
    
    # Show help if enabled
    if show_help:
        draw_help()

def draw_help():
    """Draw help information overlay"""
    # Semi-transparent background
    help_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    help_surface.fill((0, 0, 0, 220))
    screen.blit(help_surface, (0, 0))
    
    # Help content
    help_title = title_font.render("L-System Generator Help", True, WHITE)
    screen.blit(help_title, (WIDTH/2 - help_title.get_width()/2, 80))
    
    help_texts = [
        "L-systems (Lindenmayer systems) are string rewriting systems used to model plant growth and generate fractals.",
        "",
        "Controls:",
        "- Generate: Create and draw the L-system based on current settings",
        "- Previous/Next System: Switch between the four predefined L-systems",
        "- Decrease/Increase Iterations: Change the complexity of the fractal",
        "- Auto Center: Toggle automatic centering and scaling of the fractal",
        "",
        "Symbols:",
        "F - Draw forward",
        "b - Move forward without drawing",
        "+ - Turn right by the specified angle",
        "- - Turn left by the specified angle",
        "[ - Save the current position and angle",
        "] - Return to the previously saved position and angle",
        "",
        "Press any key or click to close this help."
    ]
    
    for i, text in enumerate(help_texts):
        help_text = font.render(text, True, WHITE)
        screen.blit(help_text, (WIDTH/2 - 200, 130 + i * 25))

def check_button_click(pos):
    """Check if a button was clicked and handle the action"""
    global current_system, iterations, auto_center, fractal_string, show_help
    
    x, y = pos
    if x < 20 or x > 260:  # Outside button area
        return
    
    # Generate button
    if 220 <= y <= 250:
        regenerate_fractal()
    
    # Previous System button
    elif 260 <= y <= 290:
        current_system = (current_system - 1) % len(l_systems)
        fractal_string = l_systems[current_system]["axiom"]
    
    # Next System button
    elif 300 <= y <= 330:
        current_system = (current_system + 1) % len(l_systems)
        fractal_string = l_systems[current_system]["axiom"]
    
    # Decrease Iterations button
    elif 340 <= y <= 370 and iterations > 1:
        iterations -= 1
    
    # Increase Iterations button
    elif 380 <= y <= 410:
        iterations += 1
    
    # Auto Center toggle
    elif 420 <= y <= 450:
        auto_center = not auto_center
    
    # Show Help
    elif 460 <= y <= 490:
        show_help = True

def regenerate_fractal():
    """Regenerate the fractal with current settings"""
    global fractal_string
    
    # Get current system parameters
    system = l_systems[current_system]
    
    # Generate new fractal string
    fractal_string = generate_l_system(system["axiom"], system["rules"], iterations)
    
    # Clear screen and draw UI
    screen.fill(BLACK)
    draw_ui()
    
    # Draw the L-system
    draw_l_system(
        fractal_string,
        system["angle"],
        system["initial_angle"],
        system["length"],
        system["color"]
    )

# Main loop
def main():
    global show_help
    clock = pygame.time.Clock()
    regenerate_fractal()  # Initial generation
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not drawing:
                if show_help:
                    show_help = False
                else:
                    check_button_click(event.pos)
                    # Redraw everything
                    screen.fill(BLACK)
                    draw_ui()
                    
                    # If we're not showing help, redraw the current fractal
                    if not show_help and fractal_string:
                        system = l_systems[current_system]
                        draw_l_system(
                            fractal_string,
                            system["angle"],
                            system["initial_angle"],
                            system["length"],
                            system["color"]
                        )
            
            elif event.type == pygame.KEYDOWN and show_help:
                show_help = False
                # Redraw everything
                screen.fill(BLACK)
                draw_ui()
                
                if fractal_string:
                    system = l_systems[current_system]
                    draw_l_system(
                        fractal_string,
                        system["angle"],
                        system["initial_angle"],
                        system["length"],
                        system["color"]
                    )
        
        # Update display
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
