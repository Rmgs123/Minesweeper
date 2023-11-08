import pygame
import random
import time

# Game Constants
WIDTH = 800
HEIGHT = 800
ROWS = 10
COLS = 10
MINE_COUNT = 10
CELL_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Create the grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flags = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Place mines randomly
mine_positions = random.sample(range(ROWS * COLS), MINE_COUNT)
for position in mine_positions:
    row = position // COLS
    col = position % COLS
    grid[row][col] = -1  # -1 -> mine

# Calculate numbers for cells
for row in range(ROWS):
    for col in range(COLS):
        if grid[row][col] != -1:
            count = 0
            for i in range(max(0, row - 1), min(row + 2, ROWS)):
                for j in range(max(0, col - 1), min(col + 2, COLS)):
                    if grid[i][j] == -1:
                        count += 1
            grid[row][col] = count

# Function to reveal adjacent safe cells
def reveal_adjacent_safe_cells(row, col):
    for i, j in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= i < ROWS and 0 <= j < COLS and not revealed[i][j]:
            revealed[i][j] = True
            if grid[i][j] == 0:
                reveal_adjacent_safe_cells(i, j)

def check_victory():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1 and not revealed[row][col]:
                return False
            if grid[row][col] == -1 and not flags[row][col]:
                return False
    return True

# Main game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                if grid[row][col] == -1:  # Lost by mine click
                    revealed = [[True for _ in range(COLS)] for _ in range(ROWS)]
                    game_over = True
                else:
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        if grid[row][col] == 0:
                            reveal_adjacent_safe_cells(row, col)
            elif event.button == 3:  # Right mouse button
                x, y = event.pos
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                if not revealed[row][col]:
                    flags[row][col] = not flags[row][col]

    win.fill(WHITE)

    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Draw cell
            if revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.rect(win, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif grid[row][col] == 0:
                    pygame.draw.rect(win, DARK_GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(win, DARK_GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                    font = pygame.font.Font(None, CELL_SIZE // 2)
                    text = font.render(str(grid[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    win.blit(text, text_rect)
            else:
                pygame.draw.rect(win, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                if flags[row][col]:
                    pygame.draw.circle(win, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
                    
    if not game_over and check_victory():
        font = pygame.font.Font(None, 100)
        text = font.render("You won!", True, (255, 225, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)
        pygame.display.update()
        game_over = True
        time.sleep(6)

    pygame.display.update()

pygame.quit()