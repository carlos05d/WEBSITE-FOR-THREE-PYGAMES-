import pygame
import random

# إعداد Pygame
pygame.init()

# إعدادات الشاشة
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# الألوان
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
COLOR_LIST = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE]

# الأشكال
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],  # O-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 0, 0], [1, 1, 1]],  # L-shape
    [[0, 0, 1], [1, 1, 1]]   # J-shape
]

# فئة للكتلة
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = SCREEN_WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# الشبكة
def create_grid():
    grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    return grid

def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]:
                pygame.draw.rect(screen, COLOR_LIST[grid[i][j] - 1], 
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for i in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (i, 0), (i, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, i), (SCREEN_WIDTH, i))

# تحريك القطعة
def check_collision(grid, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                x_pos = (tetromino.x + j * BLOCK_SIZE) // BLOCK_SIZE
                y_pos = (tetromino.y + i * BLOCK_SIZE) // BLOCK_SIZE
                if x_pos < 0 or x_pos >= SCREEN_WIDTH // BLOCK_SIZE or y_pos >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if y_pos >= 0 and grid[y_pos][x_pos]:
                    return True
    return False

def clear_rows(grid):
    full_rows = []
    for i, row in enumerate(grid):
        if all(cell != 0 for cell in row):
            full_rows.append(i)
    for i in full_rows:
        grid.pop(i)
        grid.insert(0, [0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
    return len(full_rows)

# اللعبة الرئيسية
def main():
    clock = pygame.time.Clock()
    grid = create_grid()
    score = 0
    game_over = False
    current_tetromino = Tetromino(random.choice(SHAPES), random.choice(COLOR_LIST))
    next_tetromino = Tetromino(random.choice(SHAPES), random.choice(COLOR_LIST))
    speed = 10  # سرعة اللعبة
    while not game_over:
        screen.fill((0, 0, 0))

        # التعامل مع الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= BLOCK_SIZE
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x += BLOCK_SIZE
                if event.key == pygame.K_RIGHT:
                    current_tetromino.x += BLOCK_SIZE
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x -= BLOCK_SIZE
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += BLOCK_SIZE
                    if check_collision(grid, current_tetromino):
                        current_tetromino.y -= BLOCK_SIZE
                if event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if check_collision(grid, current_tetromino):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                if event.key == pygame.K_r and game_over:  # إذا تم الضغط على R لإعادة اللعبة
                    main()

        # تحريك القطعة لأسفل
        current_tetromino.y += BLOCK_SIZE
        if check_collision(grid, current_tetromino):
            current_tetromino.y -= BLOCK_SIZE
            for i, row in enumerate(current_tetromino.shape):
                for j, cell in enumerate(row):
                    if cell:
                        x_pos = (current_tetromino.x + j * BLOCK_SIZE) // BLOCK_SIZE
                        y_pos = (current_tetromino.y + i * BLOCK_SIZE) // BLOCK_SIZE
                        grid[y_pos][x_pos] = COLOR_LIST.index(current_tetromino.color) + 1
            score += clear_rows(grid) * 100  # إضافة النقاط بناءً على الصفوف التي تم مسحها
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(random.choice(SHAPES), random.choice(COLOR_LIST))
            if check_collision(grid, current_tetromino):
                game_over = True

        # زيادة السرعة تدريجيًا بعد كل مسح لصفوف
        if score // 1000 > speed // 10:
            speed += 1

        # الرسم
        draw_grid(grid)
        current_tetromino.draw()

        # عرض النتيجة
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # عرض Game Over
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

        pygame.display.update()
        clock.tick(speed)  # تعديل السرعة

    pygame.quit()

if __name__ == "__main__":
    main()
