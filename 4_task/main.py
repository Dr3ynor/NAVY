import pygame
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import os

# === Konfigurace ===
WIDTH, HEIGHT = 1280, 900
ROWS, COLS = 6, 6
CELL_SIZE = 80
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE

# Pozice panelů
EDIT_PANEL_X = BOARD_WIDTH + 20
HISTORY_PANEL_X = 20
HISTORY_PANEL_Y = BOARD_HEIGHT + 20

# Barvy
WALKER_COLOR = (0, 255, 0)
CHEESE_COLOR = (255, 223, 0)
HOLE_COLOR = (100, 100, 100)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (70, 70, 70)
BUTTON_COLOR = (80, 80, 200)
BUTTON_HOVER = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
INFO_COLOR = (200, 200, 200)
PANEL_COLOR = (50, 50, 50)
PATH_COLOR = (0, 180, 0, 128)
MODE_COLORS = {
    "place_cheese": CHEESE_COLOR,
    "place_hole": HOLE_COLOR,
    "erase": (200, 50, 50)
}

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Cheese – Q-learning")
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

def create_board():
    board = np.full((ROWS, COLS), ' ')
    board[5, 5] = 'C'  # výchozí pozice sýra
    board[1, 3] = 'O'
    board[2, 2] = 'O'
    board[3, 4] = 'O'
    board[4, 1] = 'O'
    return board

board = create_board()
walker_pos = [0, 0]
edit_mode = None

# Vizualizace učení
agent_path = []  # Historie pohybu agenta pro vizualizaci
training_in_progress = False
current_episode = 0
current_step = 0
episode_successes = 0
training_speed = 5  # Rychlost vizualizace (kroky za frame)
show_path = True  # Přepínač pro zobrazení cesty
show_values = False  # Přepínač pro zobrazení Q-hodnot

# === Q-learning ===
Q = np.zeros((ROWS, COLS, 4))  # 4 akce: R, L, D, U
actions = [(0,1),(0,-1),(1,0),(-1,0)]  # R, L, D, U
action_names = ["Vpravo", "Vlevo", "Dolů", "Nahoru"]
action_symbols = ["→", "←", "↓", "↑"]  # Symboly pro vizualizaci

alpha = 0.1  # Rychlost učení
gamma = 0.9  # Discount faktor
epsilon = 0.1  # Explorační faktor

# Historie pro graf
history = {
    'episodes': [],
    'steps': [],
    'rewards': [],
    'success_rate': [],
    'paths': []  # Pro ukládání cest agenta
}

def choose_action(y, x, greedy=False):
    if not greedy and random.random() < epsilon:
        return random.randint(0, 3)
    return np.argmax(Q[y, x])

def get_reward(y, x):
    if board[y, x] == 'C':
        return 10
    elif board[y, x] == 'O':
        return -10
    return -0.1

def train_step():
    global current_episode, current_step, walker_pos, agent_path, episode_successes, training_in_progress
    
    # Pokud začínáme novou epizodu
    if current_step == 0:
        walker_pos = [0, 0]
        agent_path = [(0, 0)]
    
    # Jeden krok Q-learningu
    y, x = walker_pos
    a = choose_action(y, x)
    dy, dx = actions[a]
    ny, nx = y + dy, x + dx
    
    # Hranice mapy
    if not (0 <= ny < ROWS and 0 <= nx < COLS):
        ny, nx = y, x
        
    # Aktualizace agenta
    walker_pos = [ny, nx]
    agent_path.append((nx, ny))  # Přidáme do historie cesty (x, y) pro vizualizaci
    
    # Výpočet odměny a aktualizace Q-tabulky
    r = get_reward(ny, nx)
    Q[y, x, a] = Q[y, x, a] + alpha * (r + gamma * np.max(Q[ny, nx]) - Q[y, x, a])
    
    # Kontrola ukončení epizody
    current_step += 1
    episode_ended = False
    
    if board[ny, nx] == 'C':  # Sýr nalezen - úspěch
        episode_ended = True
        episode_successes += 1
    elif board[ny, nx] == 'O':  # Díra - neúspěch
        episode_ended = True
    elif current_step >= 100:  # Limit kroků - neúspěch
        episode_ended = True
    
    # Pokud epizoda skončila, připravíme se na další
    if episode_ended:
        # Uložíme cestu a reset pro další epizodu
        current_episode += 1
        if len(history['paths']) <= current_episode:
            history['paths'].append(agent_path.copy())
        current_step = 0
        
        # Konec tréninku po dosažení počtu epizod
        if current_episode >= 50:
            # Aktualizace historie
            if len(history['episodes']) == 0:
                start_ep = 1
            else:
                start_ep = history['episodes'][-1] + 1
                
            new_episodes = list(range(start_ep, start_ep + 50))
            history['episodes'].extend(new_episodes)
            history['success_rate'].append(episode_successes / 50 * 100)
            
            # Reset pro příští trénink
            episode_successes = 0
            current_episode = 0
            training_in_progress = False
            update_history_graph()
    
    return episode_ended

def update_history_graph():
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    
    # Graf úspěšnosti
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    x = list(range(1, len(history['success_rate'])+1))
    ax.plot(x, history['success_rate'], 'g-')
    ax.set_title('Úspěšnost trénování')
    ax.set_xlabel('Tréninkový cyklus')
    ax.set_ylabel('Úspěšnost (%)')
    ax.grid(True)
    ax.set_ylim(0, 100)
    
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()
    
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    pygame.image.save(surf, "graphs/success_history.png")

def reset_game():
    global walker_pos, agent_path
    walker_pos = [0, 0]
    agent_path = [(0, 0)]

def reset_q_learning():
    global Q, history, current_episode, current_step, episode_successes
    Q = np.zeros((ROWS, COLS, 4))
    history = {
        'episodes': [],
        'steps': [],
        'rewards': [],
        'success_rate': [],
        'paths': []
    }
    current_episode = 0
    current_step = 0
    episode_successes = 0

# === GUI ===
def draw_board():
    # Pozadí herní plochy
    pygame.draw.rect(win, BG_COLOR, (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
    
    # Vizualizace Q-hodnot a cesta agenta
    if show_path and agent_path:
        # Vykreslení cesty agenta
        for i in range(1, len(agent_path)):
            start = agent_path[i-1]
            end = agent_path[i]
            start_pos = (start[0] * CELL_SIZE + CELL_SIZE//2, start[1] * CELL_SIZE + CELL_SIZE//2)
            end_pos = (end[0] * CELL_SIZE + CELL_SIZE//2, end[1] * CELL_SIZE + CELL_SIZE//2)
            pygame.draw.line(win, PATH_COLOR, start_pos, end_pos, 4)
            pygame.draw.circle(win, PATH_COLOR, start_pos, 4)
    
    # Mřížka a obsah buněk
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(win, GRID_COLOR, rect, 1)
            
            # Zobrazení Q-hodnot v každé buňce
            if show_values:
                for i, (dy, dx) in enumerate(actions):
                    value = Q[y, x, i]
                    if abs(value) > 0.01:  # Zobrazit jen nenulové hodnoty
                        # Pozice pro text hodnot
                        text_x = x * CELL_SIZE + CELL_SIZE//2
                        text_y = y * CELL_SIZE + CELL_SIZE//2
                        
                        # Posunout podle směru akce
                        offset = 14
                        if i == 0:  # Vpravo
                            text_x += offset
                        elif i == 1:  # Vlevo
                            text_x -= offset
                        elif i == 2:  # Dolů
                            text_y += offset
                        elif i == 3:  # Nahoru
                            text_y -= offset
                        
                        # Barva podle hodnoty
                        if value > 0:
                            color = (0, min(255, int(value * 50)), 0)
                        else:
                            color = (min(255, int(-value * 50)), 0, 0)
                        
                        # Zobrazení hodnoty a symbolu
                        q_text = small_font.render(f"{action_symbols[i]}{value:.1f}", True, color)
                        win.blit(q_text, (text_x - q_text.get_width()//2, text_y - q_text.get_height()//2))
            
            # Obsah buňky
            cell = board[y, x]
            if cell == 'C':
                pygame.draw.circle(win, CHEESE_COLOR, rect.center, CELL_SIZE//3)
                cheese_img = small_font.render("Sýr", True, BG_COLOR)
                win.blit(cheese_img, (rect.center[0] - cheese_img.get_width()//2, rect.center[1] - cheese_img.get_height()//2))
            elif cell == 'O':
                pygame.draw.circle(win, HOLE_COLOR, rect.center, CELL_SIZE//3)
                hole_img = small_font.render("Díra", True, TEXT_COLOR)
                win.blit(hole_img, (rect.center[0] - hole_img.get_width()//2, rect.center[1] - hole_img.get_height()//2))

    # Agent
    wx, wy = walker_pos[1], walker_pos[0]
    rect = pygame.Rect(wx*CELL_SIZE, wy*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.circle(win, WALKER_COLOR, rect.center, CELL_SIZE//3)
    agent_img = small_font.render("Agent", True, BG_COLOR)
    win.blit(agent_img, (rect.center[0] - agent_img.get_width()//2, rect.center[1] - agent_img.get_height()//2))

def draw_button(text, x, y, w, h, hovered, active=False):
    rect = pygame.Rect(x, y, w, h)
    if active:
        color = (50, 180, 50)
    elif hovered:
        color = BUTTON_HOVER
    else:
        color = BUTTON_COLOR
    pygame.draw.rect(win, color, rect)
    label = font.render(text, True, TEXT_COLOR)
    win.blit(label, (x + (w - label.get_width())//2, y + (h - label.get_height())//2))
    return rect

def draw_edit_panel():
    # Panel pozadí
    pygame.draw.rect(win, PANEL_COLOR, (BOARD_WIDTH, 0, WIDTH - BOARD_WIDTH, HEIGHT))
    
    # Nadpis
    title = font.render("Nastavení mapy", True, TEXT_COLOR)
    win.blit(title, (EDIT_PANEL_X, 20))
    
    panel_buttons = []
    button_width = 160
    button_height = 35
    button_gap = 10
    
    # Tlačítka pro úpravy mapy
    y_pos = 60
    
    cheese_btn = draw_button("Přidat sýr", EDIT_PANEL_X, y_pos, button_width, button_height, 
                             pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                             active=(edit_mode == "place_cheese"))
    panel_buttons.append(("place_cheese", cheese_btn))
    y_pos += button_height + button_gap
    
    hole_btn = draw_button("Přidat díru", EDIT_PANEL_X, y_pos, button_width, button_height, 
                           pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                           active=(edit_mode == "place_hole"))
    panel_buttons.append(("place_hole", hole_btn))
    y_pos += button_height + button_gap
    
    erase_btn = draw_button("Vymazat", EDIT_PANEL_X, y_pos, button_width, button_height, 
                            pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                            active=(edit_mode == "erase"))
    panel_buttons.append(("erase", erase_btn))
    y_pos += button_height + 20
    
    # Nadpis pro Q-learning
    q_title = font.render("Q-learning", True, TEXT_COLOR)
    win.blit(q_title, (EDIT_PANEL_X, y_pos))
    y_pos += 30
    
    # Tlačítka pro Q-learning
    train_btn = draw_button("Trénovat (50 ep.)", EDIT_PANEL_X, y_pos, button_width, button_height,
                           pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                           active=training_in_progress)
    panel_buttons.append(("train", train_btn))
    y_pos += button_height + button_gap
    
    run_btn = draw_button("Spustit agenta", EDIT_PANEL_X, y_pos, button_width, button_height,
                         pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                         active=running_agent)
    panel_buttons.append(("run", run_btn))
    y_pos += button_height + button_gap
    
    reset_btn = draw_button("Resetovat agenta", EDIT_PANEL_X, y_pos, button_width, button_height,
                           pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse))
    panel_buttons.append(("reset", reset_btn))
    y_pos += button_height + button_gap
    
    reset_q_btn = draw_button("Resetovat Q-tabulku", EDIT_PANEL_X, y_pos, button_width, button_height,
                             pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse))
    panel_buttons.append(("reset_q", reset_q_btn))
    y_pos += button_height + 20
    
    # Vizualizační nastavení
    vis_title = font.render("Vizualizace", True, TEXT_COLOR)
    win.blit(vis_title, (EDIT_PANEL_X, y_pos))
    y_pos += 30
    
    path_btn = draw_button("Zobrazit cestu", EDIT_PANEL_X, y_pos, button_width, button_height,
                          pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                          active=show_path)
    panel_buttons.append(("toggle_path", path_btn))
    y_pos += button_height + button_gap
    
    values_btn = draw_button("Zobrazit hodnoty", EDIT_PANEL_X, y_pos, button_width, button_height,
                            pygame.Rect(EDIT_PANEL_X, y_pos, button_width, button_height).collidepoint(mouse),
                            active=show_values)
    panel_buttons.append(("toggle_values", values_btn))
    y_pos += button_height + button_gap
    
    # Tlačítka pro rychlost vizualizace
    speed_label = small_font.render(f"Rychlost: {training_speed}x", True, INFO_COLOR)
    win.blit(speed_label, (EDIT_PANEL_X, y_pos))
    y_pos += 25
    
    speed_down_btn = draw_button("-", EDIT_PANEL_X, y_pos, 40, button_height,
                               pygame.Rect(EDIT_PANEL_X, y_pos, 40, button_height).collidepoint(mouse))
    panel_buttons.append(("speed_down", speed_down_btn))
    
    speed_up_btn = draw_button("+", EDIT_PANEL_X + 50, y_pos, 40, button_height,
                             pygame.Rect(EDIT_PANEL_X + 50, y_pos, 40, button_height).collidepoint(mouse))
    panel_buttons.append(("speed_up", speed_up_btn))
    y_pos += button_height + 20
    
    # Informace o aktuálním stavu
    info_title = font.render("Informace", True, TEXT_COLOR)
    win.blit(info_title, (EDIT_PANEL_X, y_pos))
    y_pos += 30
    
    y, x = walker_pos
    if 0 <= y < ROWS and 0 <= x < COLS:
        q_values = Q[y, x]
        max_q = np.max(q_values)
        best_action = np.argmax(q_values)
        
        position_info = small_font.render(f"Pozice agenta: [{x}, {y}]", True, INFO_COLOR)
        win.blit(position_info, (EDIT_PANEL_X, y_pos))
        y_pos += 25
        
        # Zobrazení stavu tréninku
        if training_in_progress:
            train_info = small_font.render(f"Trénink: Epizoda {current_episode+1}/50", True, INFO_COLOR)
            win.blit(train_info, (EDIT_PANEL_X, y_pos))
            y_pos += 25
            
            steps_info = small_font.render(f"Krok: {current_step}", True, INFO_COLOR)
            win.blit(steps_info, (EDIT_PANEL_X, y_pos))
            y_pos += 25
            
            success_info = small_font.render(f"Úspěchů: {episode_successes}", True, INFO_COLOR)
            win.blit(success_info, (EDIT_PANEL_X, y_pos))
            y_pos += 25
        
        # Zobrazení Q-hodnot pro aktuální pozici
        q_info = small_font.render("Q-hodnoty:", True, INFO_COLOR)
        win.blit(q_info, (EDIT_PANEL_X, y_pos))
        y_pos += 25
        
        for i, (action, value) in enumerate(zip(action_names, q_values)):
            color = TEXT_COLOR if i == best_action else INFO_COLOR
            action_text = small_font.render(f"{action_symbols[i]} {action}: {value:.2f}", True, color)
            win.blit(action_text, (EDIT_PANEL_X, y_pos))
            y_pos += 20
    
    return panel_buttons

def draw_history_panel():
    # Vykreslit historii pokud existují grafy
    if os.path.exists("graphs/success_history.png"):
        history_title = font.render("Historie učení", True, TEXT_COLOR)
        win.blit(history_title, (HISTORY_PANEL_X, HISTORY_PANEL_Y))
        
        # Informace o úspěšnosti posledního tréninku
        if history['success_rate']:
            success_text = small_font.render(
                f"Poslední úspěšnost: {history['success_rate'][-1]:.1f}%", 
                True, INFO_COLOR
            )
            win.blit(success_text, (HISTORY_PANEL_X, HISTORY_PANEL_Y + 30))
        
        # Vykreslení grafu úspěšnosti
        if os.path.exists("graphs/success_history.png"):
            success_graph = pygame.image.load("graphs/success_history.png")
            success_graph = pygame.transform.scale(success_graph, (400, 200))
            win.blit(success_graph, (HISTORY_PANEL_X, HISTORY_PANEL_Y + 60))

def move_agent():
    global walker_pos, agent_path
    y, x = walker_pos
    a = choose_action(y, x, greedy=True)  # Použijeme greedy volbu
    dy, dx = actions[a]
    ny, nx = y + dy, x + dx
    if 0 <= ny < ROWS and 0 <= nx < COLS:
        walker_pos = [ny, nx]
        agent_path.append((nx, ny))

def edit_board(pos):
    global board
    if pos[0] < BOARD_WIDTH and pos[1] < BOARD_HEIGHT:
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        
        if edit_mode == "place_cheese":
            # Odstranit předchozí sýr
            for r in range(ROWS):
                for c in range(COLS):
                    if board[r, c] == 'C':
                        board[r, c] = ' '
            board[y, x] = 'C'
        elif edit_mode == "place_hole":
            if board[y, x] != 'C':  # Nenahrazujeme sýr dírou
                board[y, x] = 'O'
        elif edit_mode == "erase":
            if board[y, x] != 'C' or count_cheese() > 1:  # Neodstraňujeme poslední sýr
                board[y, x] = ' '

def count_cheese():
    count = 0
    for r in range(ROWS):
        for c in range(COLS):
            if board[r, c] == 'C':
                count += 1
    return count

# === Main loop ===
clock = pygame.time.Clock()
running = True
running_agent = False
last_agent_move_time = 0
agent_move_delay = 200  # ms

while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    win.fill(BG_COLOR)
    draw_board()
    panel_buttons = draw_edit_panel()
    draw_history_panel()

    if click:
        # Obsluha tlačítek v panelu
        for button_id, button_rect in panel_buttons:
            if button_rect.collidepoint(mouse):
                if button_id in ["place_cheese", "place_hole", "erase"]:
                    edit_mode = button_id if edit_mode != button_id else None
                elif button_id == "train":
                    training_in_progress = not training_in_progress
                    if training_in_progress:
                        reset_game()
                        current_episode = 0
                        current_step = 0
                        episode_successes = 0
                elif button_id == "run":
                    running_agent = not running_agent
                    if running_agent:
                        reset_game()
                elif button_id == "reset":
                    reset_game()
                    running_agent = False
                elif button_id == "reset_q":
                    reset_q_learning()
                    reset_game()
                    running_agent = False
                    training_in_progress = False
                elif button_id == "toggle_path":
                    show_path = not show_path
                elif button_id == "toggle_values":
                    show_values = not show_values
                elif button_id == "speed_up":
                    training_speed = min(20, training_speed + 1)
                elif button_id == "speed_down":
                    training_speed = max(1, training_speed - 1)
                break
        
        # Úprava herní plochy, pokud je aktivní režim úprav
        if edit_mode in ["place_cheese", "place_hole", "erase"]:
            edit_board(mouse)

    # Vizualizace učení agenta
    if training_in_progress:
        # Provádíme několik kroků učení (podle rychlosti)
        for _ in range(training_speed):
            if current_episode < 50:
                train_step()
            else:
                training_in_progress = False
                break

    # Pohyb agenta v demo režimu
    if running_agent:
        current_time = pygame.time.get_ticks()
        if current_time - last_agent_move_time > agent_move_delay:
            move_agent()
            last_agent_move_time = current_time
            
            y, x = walker_pos
            if board[y, x] == 'C':
                pygame.time.wait(500)  # Krátká pauza při nalezení sýra
                reset_game()
            elif board[y, x] == 'O':
                pygame.time.wait(500)  # Krátká pauza při spadnutí do díry
                reset_game()

    pygame.display.update()

pygame.quit()
