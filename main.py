import pygame 
import sys
import os
from player import player
from floor import floor
from platform import platform
from enemy import enemy

# --- PyInstaller Asset Path Fix ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

# --- Music ---
pygame.mixer.music.load(resource_path("assets/music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# --- Window Setup ---
win_w = 800
win_h = 600
win = pygame.display.set_mode((win_w, win_h), pygame.SCALED, pygame.DOUBLEBUF)
pygame.display.set_caption('The Revenge of Farts')
fps = 60
clock = pygame.time.Clock()
score_font = pygame.font.Font(resource_path('assets/font.ttf'), 20)

# --- UI Functions ---
def bg_fill(win_w, win_h, win):
    win.fill((0, 0, 0)) 

def bg_remove(win_w, win_h, color):
    fill_object = pygame.Rect(0, 0, win_w, win_h)
    pygame.Surface.fill(win, color, fill_object)

def board_text(text, font, text_color, x, y):
    text_to_img = font.render(text, True, text_color)
    win.blit(text_to_img, (x, y))

def draw_ui(surface, player):
    max_masks = 10
    current_masks = player.player_health // 10
    
    for i in range(max_masks):
        x = 30 + (i * 35)
        y = 30
        
        if i < current_masks:
            pygame.draw.circle(surface, (255, 255, 255), (x, y), 12)
        else:
            pygame.draw.circle(surface, (100, 100, 100), (x, y), 12, 2)

def check_if_player_is_dead(player):
    if player.player_health <= 0:
        return True
    return False

def check_if_enemy_is_dead(enemy):
    if enemy.health <= 0:
        return True
    return False

# --- Game Setup ---
camera_x = 0
camera_y = 0
level_width = 2000
level_height = 600

platforms = [
    platform(300, 450, 200, 20, win),
    platform(650, 350, 150, 20, win),
    platform(1000, 250, 200, 20, win),
    platform(1400, 400, 300, 20, win),
    platform(1800, 300, 150, 20, win)
]

player_obj = player(10, win_h - 175, win)
floor_obj = floor(level_width, win_h, win)
enemy1 = enemy(win, level_width, win_h)

lose = False
e_lose = False

# --- Reset Function ---
def reset_game():
    global camera_x, camera_y, lose, e_lose
    
    # Reset Player
    player_obj.player_health = 100
    player_obj.player_base.x = 10
    player_obj.player_base.y = win_h - 175
    player_obj.dx = 0
    player_obj.dy = 0
    player_obj.invincible = False
    player_obj.is_att = False
    player_obj.color = (255, 255, 255)
    player_obj.state = "IDLE"
    
    # Reset Enemy
    enemy1.health = 100
    enemy1.eb.x = 200
    enemy1.eb.y = win_h - 175
    enemy1.dx = 0
    
    # Reset Camera & States
    camera_x = 0
    camera_y = 0
    lose = False
    e_lose = False
    pygame.display.set_caption('The Revenge of Farts')
    print("Game Reset!")

# --- Game Loop ---
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    # 1. Update Objects
    player_obj.move(win_w, win_h, floor_obj, platforms, enemy1, camera_x, camera_y)
    enemy1.move(floor_obj, player_obj)

    # 2. Camera Logic (Lerp & Clamp)
    t_camera_x = player_obj.player_base.centerx - win_w // 2
    t_camera_y = player_obj.player_base.centery - win_h // 2
    camera_x += (t_camera_x - camera_x) * 0.1
    camera_y += (t_camera_y - camera_y) * 0.1

    if camera_x < 0:
        camera_x = 0
    if camera_x > level_width - win_w:
        camera_x = level_width - win_w
    if camera_y < 0:
        camera_y = 0
    if camera_y > level_height - win_h:
        camera_y = level_height - win_h

    # 3. Draw Everything
    bg_fill(win_w, win_h, win)
    floor_obj.draw(camera_x, camera_y)
    enemy1.draw(camera_x, camera_y)
    player_obj.draw(camera_x, camera_y)

    for p in platforms:
        p.draw((0, 0, 200), camera_x, camera_y)

    draw_ui(win, player_obj)

    # 4. Check Win/Loss Conditions
    lose = check_if_player_is_dead(player_obj)
    e_lose = check_if_enemy_is_dead(enemy1)
    
    if lose:
        bg_remove(win_w, win_h, (100, 0, 0))
        board_text('YOU LOSE', score_font, (0, 0, 0), win_w // 2 - 40, win_h // 2)
        board_text('press R to restart', score_font, (0, 0, 0), win_w // 2 - 60, win_h // 2 + 40)
    if e_lose:
        bg_remove(win_w, win_h, (0, 100, 0))
        board_text('YOU WIN', score_font, (0, 0, 0), win_w // 2 - 40, win_h // 2)
        board_text('press R to restart', score_font, (0, 0, 0), win_w // 2 - 60, win_h // 2 + 40)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()