# 🟩🟥 2D Grid Chase Game - Fixed Version
import pygame
import sys

# ----- Initialize Pygame -----
pygame.init()

# ----- Grid settings -----
grid_size = 50
grid_width = 10
grid_height = 5
BUTTON_SECTION_HEIGHT = 150  # Variable for extra space
screen_width = grid_width * grid_size
screen_height = (grid_height * grid_size) + BUTTON_SECTION_HEIGHT

# ----- Colors -----
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)   # Player
RED = (255, 0, 0)     # Enemy
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # Buttons

# ----- Screen -----
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Grid Chase Game")

# ----- Player & Enemy positions -----
player_x, player_y = 2, 2
enemy_x, enemy_y = 7, 4

# ----- Clock & enemy timer -----
clock = pygame.time.Clock()
enemy_timer = 0  # controls AI speed

# ----- Touch button setup -----
button_size = 50
button_y = grid_height * grid_size + 20

up_button = pygame.Rect(screen_width//2, button_y, button_size, button_size)
down_button = pygame.Rect(screen_width//2, button_y + button_size*2, button_size, button_size)
left_button = pygame.Rect(screen_width//2 - button_size*2, button_y + button_size, button_size, button_size)
right_button = pygame.Rect(screen_width//2 + button_size*2, button_y + button_size, button_size, button_size)

# ----- Draw everything -----
def draw_grid():
    screen.fill(WHITE)
    # Grid lines
    for x in range(0, grid_width*grid_size, grid_size):
        pygame.draw.line(screen, BLACK, (x,0), (x,grid_height*grid_size))
    for y in range(0, grid_height*grid_size, grid_size):
        pygame.draw.line(screen, BLACK, (0,y), (grid_width*grid_size,y))
    # Player & Enemy
    pygame.draw.rect(screen, GREEN, (player_x*grid_size, player_y*grid_size, grid_size, grid_size))
    pygame.draw.rect(screen, RED, (enemy_x*grid_size, enemy_y*grid_size, grid_size, grid_size))
    # Buttons
    pygame.draw.rect(screen, GRAY, up_button)
    pygame.draw.rect(screen, GRAY, down_button)
    pygame.draw.rect(screen, GRAY, left_button)
    pygame.draw.rect(screen, GRAY, right_button)
    # Labels
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render("↑", True, BLACK), (up_button.x+15, up_button.y+10))
    screen.blit(font.render("↓", True, BLACK), (down_button.x+15, down_button.y+10))
    screen.blit(font.render("←", True, BLACK), (left_button.x+15, left_button.y+10))
    screen.blit(font.render("→", True, BLACK), (right_button.x+15, right_button.y+10))
    pygame.display.flip()

# ----- Enemy AI -----
def move_enemy():
    global enemy_x, enemy_y
    if enemy_x > player_x:
        enemy_x -= 1
    elif enemy_x < player_x:
        enemy_x += 1
    if enemy_y > player_y:
        enemy_y -= 1
    elif enemy_y < player_y:
        enemy_y += 1

# ----- Main Game Loop -----
running = True
while running:
    draw_grid()
    enemy_timer += 1  # increment timer each frame

    # --- Player Input (Keyboard) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 1
    if keys[pygame.K_s] and player_y < grid_height - 1:
        player_y += 1
    if keys[pygame.K_a] and player_x > 0:
        player_x -= 1
    if keys[pygame.K_d] and player_x < grid_width - 1:
        player_x += 1

    # --- Player Input (Touch/Mouse) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if up_button.collidepoint(mx,my) and player_y > 0:
                player_y -= 1
            elif down_button.collidepoint(mx,my) and player_y < grid_height - 1:
                player_y += 1
            elif left_button.collidepoint(mx,my) and player_x > 0:
                player_x -= 1
            elif right_button.collidepoint(mx,my) and player_x < grid_width - 1:
                player_x += 1

    # --- Enemy moves slower than player input ---
    if enemy_timer >= 15:  # adjust this number for speed
        move_enemy()
        enemy_timer = 0

    # --- Check collision ---
    if player_x == enemy_x and player_y == enemy_y:
        print("Enemy reached the player! 😱")
        running = False

    clock.tick(15)  # game FPS, smooth and playable

pygame.quit()
sys.exit()
