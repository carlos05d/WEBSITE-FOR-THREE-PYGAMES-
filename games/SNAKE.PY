import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 24)

# Load Background Image
background_image = pygame.image.load('static/images/background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Snake and Food
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
        random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
score = 0
game_over = False
game_started = False

def draw_text(text, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def move_snake():
    global snake, food, score
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    if head == food:
        score += 10
        food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    else:
        snake.pop()

def reset_game():
    global snake, direction, food, score, game_over, game_started
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    score = 0
    game_over = False
    game_started = False

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_started:
        # Display Start Screen
        screen.blit(background_image, (0, 0))
        draw_text("Snake Game", WHITE, WIDTH // 2, HEIGHT // 3, center=True)
        draw_text("Press SPACE to Start", GREEN, WIDTH // 2, HEIGHT // 2, center=True)
        draw_text("Use Arrow Keys to Move", WHITE, WIDTH // 2, HEIGHT // 2 + 50, center=True)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_started = True
    elif not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        move_snake()

        # Check for collisions
        if (snake[0][0] < 0 or snake[0][1] < 0 or
                snake[0][0] >= WIDTH or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
            game_over = True

        # Draw Screen
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Draw Score
        draw_text(f"Score: {score}", WHITE, 10, 10)

    if game_over:
        # Display Game Over Screen
        screen.blit(background_image, (0, 0))
        draw_text("Game Over!", RED, WIDTH // 2, HEIGHT // 3, center=True)
        draw_text(f"Your Score: {score}", WHITE, WIDTH // 2, HEIGHT // 2, center=True)
        draw_text("Press R to Restart or Q to Quit", WHITE, WIDTH // 2, HEIGHT // 2 + 50, center=True)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(FPS)
