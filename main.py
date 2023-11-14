# -*- coding: utf-8 -*-

import pygame
import random

# Game Constants
WINDOW_SIZE = (800, 800)
GRID_SIZE = (int(WINDOW_SIZE[0] * 0.75), int(WINDOW_SIZE[1] * 0.75))
CELL_SIZE = GRID_SIZE[0] // 10  # Размер клетки, 10 клеток в ряд

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (150, 150, 150)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Minesweeper")

# Calculate the top-left corner of the grid to center it in the window
GRID_TOP_LEFT = ((WINDOW_SIZE[0] - GRID_SIZE[0]) // 2, (WINDOW_SIZE[1] - GRID_SIZE[1]) // 2)

# Create the grid
ROWS = GRID_SIZE[1] // CELL_SIZE
COLS = GRID_SIZE[0] // CELL_SIZE
MINE_COUNT = 20
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flags = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Function to generate the mines grid
def generate_mines():
    global grid, revealed, flags
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flags = [[False for _ in range(COLS)] for _ in range(ROWS)]

    mine_positions = random.sample(range(ROWS * COLS), MINE_COUNT)
    for position in mine_positions:
        row = position // COLS
        col = position % COLS
        grid[row][col] = -1

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
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLS)):
            if not revealed[i][j]:
                revealed[i][j] = True
                if grid[i][j] == 0:
                    reveal_adjacent_safe_cells(i, j)

# Function to check victory conditions
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
first_click = True  # Flag to track the first click
restart_rect = pygame.Rect(WINDOW_SIZE[0] // 2 - 50, 50, 100, 40)
restart_font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                row = (y - GRID_TOP_LEFT[1]) // CELL_SIZE
                col = (x - GRID_TOP_LEFT[0]) // CELL_SIZE
                if not flags[row][col]:  # Check if there is no flag
                    if first_click:
                        generate_mines()
                        while grid[row][col] != 0:  # Keep regenerating until the first click is not zero
                            generate_mines()
                        reveal_adjacent_safe_cells(row, col)
                        first_click = False
                    else:
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
                row = (y - GRID_TOP_LEFT[1]) // CELL_SIZE
                col = (x - GRID_TOP_LEFT[0]) // CELL_SIZE
                if not revealed[row][col]:
                    flags[row][col] = not flags[row][col]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                first_click = True
                game_over = False
                generate_mines()

    win.fill(WHITE)

    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_TOP_LEFT[0] + col * CELL_SIZE
            y = GRID_TOP_LEFT[1] + row * CELL_SIZE

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

    # Draw Restart Button
    pygame.draw.rect(win, GRAY, restart_rect)  # Remove white background
    restart_text = restart_font.render("Restart", True, BLACK)
    restart_rect_center = restart_text.get_rect(center=restart_rect.center)
    win.blit(restart_text, restart_rect_center)

    # Draw victory message
    if not game_over and check_victory():
        font = pygame.font.Font(None, 100)
        text = font.render("You won!", True, (255, 225, 255))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, GRID_TOP_LEFT[1] + GRID_SIZE[1] + 50))
        win.blit(text, text_rect)
        game_over = True

    # Draw grid lines
    for i in range(COLS + 1):
        pygame.draw.line(win, BLACK, (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1]),
                         (GRID_TOP_LEFT[0] + i * CELL_SIZE, GRID_TOP_LEFT[1] + GRID_SIZE[1]))
    for i in range(ROWS + 1):
        pygame.draw.line(win, BLACK, (GRID_TOP_LEFT[0], GRID_TOP_LEFT[1] + i * CELL_SIZE),
                         (GRID_TOP_LEFT[0] + GRID_SIZE[0], GRID_TOP_LEFT[1] + i * CELL_SIZE))

    pygame.display.update()

pygame.quit()