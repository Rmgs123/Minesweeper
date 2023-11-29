# -*- coding: utf-8 -*-

import pygame
import random

class MinesweeperGame:
    def __init__(self):
        self.window_size = (800, 800)
        self.grid_size = (int(self.window_size[0] * 0.75), int(self.window_size[1] * 0.75))
        self.cell_size = self.grid_size[0] // 10
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.DARK_GREEN = (0, 100, 0)
        self.GRAY = (150, 150, 150)
        # Инициализация Pygame
        pygame.init()
        self.win = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Minesweeper")

        self.calculate_grid_position()
        self.create_grid()
        self.game_over = False  # Переменная для отслеживания конца игры
        self.first_click = True  # Флаг первого клика

    def calculate_grid_position(self):
        self.grid_top_left = ((self.window_size[0] - self.grid_size[0]) // 2, (self.window_size[1] - self.grid_size[1]) // 2)

    def create_grid(self):
        self.rows = self.grid_size[1] // self.cell_size
        self.cols = self.grid_size[0] // self.cell_size
        self.mine_count = 20
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        self.generate_mines()

    def generate_mines(self):
        mines = random.sample(range(self.rows * self.cols), self.mine_count)
        for position in mines:
            row = position // self.cols
            col = position % self.cols
            self.grid[row][col] = -1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != -1:
                    count = sum(
                        self.grid[i][j] == -1
                        for i in range(max(0, row - 1), min(row + 2, self.rows))
                        for j in range(max(0, col - 1), min(col + 2, self.cols))
                    )
                    self.grid[row][col] = count

    def reveal_adjacent_safe_cells(self, row, col):
        if self.grid[row][col] == 0 and not self.revealed[row][col]:
            self.revealed[row][col] = True
            for i in range(max(0, row - 1), min(row + 2, self.rows)):
                for j in range(max(0, col - 1), min(col + 2, self.cols)):
                    self.reveal_adjacent_safe_cells(i, j)
        elif self.grid[row][col] > 0:
            self.revealed[row][col] = True

    def check_victory(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != -1 and not self.revealed[row][col]:
                    return False
                if self.grid[row][col] == -1 and not self.flags[row][col]:
                    return False
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    row = (y - self.grid_top_left[1]) // self.cell_size
                    col = (x - self.grid_top_left[0]) // self.cell_size
                    if 0 <= row < self.rows and 0 <= col < self.cols:  # Проверка корректности координат
                        if not self.flags[row][col]:
                            if self.first_click:
                                while self.grid[row][col] != 0 or self.grid[row][col] == -1:
                                    self.create_grid()
                                self.reveal_adjacent_safe_cells(row, col)
                                self.first_click = False
                            else:
                                if self.grid[row][col] == -1:
                                    self.revealed = [[True for _ in range(self.cols)] for _ in range(self.rows)]
                                    self.game_over = True
                                else:
                                    if not self.revealed[row][col]:
                                        self.revealed[row][col] = True
                                        if self.grid[row][col] == 0:
                                            self.reveal_adjacent_safe_cells(row, col)
                elif event.button == 3:  # Правая кнопка мыши
                    x, y = event.pos
                    row = (y - self.grid_top_left[1]) // self.cell_size
                    col = (x - self.grid_top_left[0]) // self.cell_size
                    if 0 <= row < self.rows and 0 <= col < self.cols:  # Проверка корректности координат
                        if not self.revealed[row][col]:
                            self.flags[row][col] = not self.flags[row][col]

    def draw_grid(self):
        self.win.fill(self.WHITE)
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.grid_top_left[0] + col * self.cell_size
                y = self.grid_top_left[1] + row * self.cell_size

                if self.revealed[row][col]:
                    if self.grid[row][col] == -1:
                        pygame.draw.rect(self.win, self.RED, (x, y, self.cell_size, self.cell_size))
                    elif self.grid[row][col] == 0:
                        pygame.draw.rect(self.win, self.DARK_GREEN, (x, y, self.cell_size, self.cell_size))
                    else:
                        pygame.draw.rect(self.win, self.DARK_GREEN, (x, y, self.cell_size, self.cell_size))
                        font = pygame.font.Font(None, self.cell_size // 2)
                        text = font.render(str(self.grid[row][col]), True, self.BLACK)
                        text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.win.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.win, self.GRAY, (x, y, self.cell_size, self.cell_size))
                    if self.flags[row][col]:
                        pygame.draw.circle(self.win, self.RED, (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 4)

        for i in range(self.cols + 1):
            pygame.draw.line(self.win, self.BLACK, (self.grid_top_left[0] + i * self.cell_size, self.grid_top_left[1]),
                             (self.grid_top_left[0] + i * self.cell_size, self.grid_top_left[1] + self.grid_size[1]))
        for i in range(self.rows + 1):
            pygame.draw.line(self.win, self.BLACK, (self.grid_top_left[0], self.grid_top_left[1] + i * self.cell_size),
                             (self.grid_top_left[0] + self.grid_size[0], self.grid_top_left[1] + i * self.cell_size))

    def run_game(self):
        running = True

        while running:
            self.handle_events()

            if self.check_victory():
                print("You won!")
                self.game_over = True

            self.draw_grid()
            pygame.display.update()

            if self.game_over:
                running = False

if __name__ == "__main__":
    minesweeper = MinesweeperGame()
    minesweeper.run_game()
