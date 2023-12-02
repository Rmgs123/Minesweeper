from re import S
import pygame
import time
import random


class MinesweeperGame:
    def __init__(self):
        self.window_size = (600, 600)
        self.grid_size = (int(self.window_size[0] * 0.75), int(self.window_size[1] * 0.75))
        self.field_size = self.rows, self.cols = (10, 10)
        self.cell_size = (self.grid_size[0] // self.cols, self.grid_size[1] // self.rows)
        self.grid_top_left = ((self.window_size[0] - self.grid_size[0]) // 2,
                              (self.window_size[1] - self.grid_size[1]) // 2)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.DARK_GREEN = (0, 100, 0)
        self.GRAY = (150, 150, 150)
        self.TEAL = (0, 128, 128)

        pygame.init()
        self.win = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Minesweeper")

        self.game_over = False
        self.first_click = True

        self.mine_count = 20
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.background_image = pygame.image.load("image1.png")
        self.field_size_value = 10
        
        self.load_field_size_value()
        
        self.font = pygame.font.Font(None, 36)
        self.settings_menu_font = pygame.font.Font(None, 36)
        self.in_settings_menu = False  
        self.generate_mines()
        
    def load_field_size_value(self):
       try:
           with open("storage.txt", "r") as file:
               self.field_size_value = int(file.read().strip())
               self.field_size = self.rows, self.cols = (self.field_size_value, self.field_size_value)
       except:
           pass
       
    def save_field_size_value(self):
        with open("storage.txt", "w") as file:
            file.write(str(self.field_size_value))

    def calculate_grid_position(self):
        self.grid_top_left = ((self.window_size[0] - self.grid_size[0]) // 2,
                              (self.window_size[1] - self.grid_size[1]) // 2)

    def generate_mines(self):
        self.load_field_size_value()
        
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
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
                if self.grid[row][col] == -1 and not self.flags[row][col] and self.revealed[row][col]:
                    return False
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 550 <= y <= 580 and 210 <= x <= 390:
                    self.game_over = True
                    continue
                if 30 <= y <= 60 and 230 <= x <= 370:
                    self.first_click = True
                    self.generate_mines()
                    continue
                row = (y - self.grid_top_left[1]) // self.cell_size[1]
                col = (x - self.grid_top_left[0]) // self.cell_size[0]
                if not (0 <= row < self.rows and 0 <= col < self.cols):
                    continue
                if event.button == 1 and not self.flags[row][col]:
                    if self.first_click:
                        while self.grid[row][col] != 0 or self.grid[row][col] == -1:
                            self.generate_mines()
                        self.reveal_adjacent_safe_cells(row, col)
                        self.first_click = False
                        continue

                    if self.grid[row][col] == -1:
                        self.revealed = [[True for _ in range(self.cols)] for _ in range(self.rows)]
                    else:
                        if self.grid[row][col] == 0:
                            self.reveal_adjacent_safe_cells(row, col)
                        self.revealed[row][col] = True
                elif event.button == 3 and not self.revealed[row][col]:
                    self.flags[row][col] = not self.flags[row][col]

    def draw_grid(self):
        self.load_field_size_value()
        
        self.win.fill(self.WHITE)
        self.win.blit(self.background_image, (0, 0))

        self.cell_size = (self.grid_size[0] // self.field_size_value, self.grid_size[1] // self.field_size_value)
        self.calculate_grid_position()

        for row in range(self.rows):
            for col in range(self.cols):
                x = self.grid_top_left[0] + col * self.cell_size[0]
                y = self.grid_top_left[1] + row * self.cell_size[1]

                if self.revealed[row][col]:
                    if self.grid[row][col] == -1:
                        pygame.draw.rect(self.win, self.RED, (x, y, self.cell_size[0], self.cell_size[1]))
                    elif self.grid[row][col] == 0:
                        pygame.draw.rect(self.win, self.DARK_GREEN, (x, y, self.cell_size[0], self.cell_size[1]))
                    else:
                        pygame.draw.rect(self.win, self.DARK_GREEN, (x, y, self.cell_size[0], self.cell_size[1]))
                        font = pygame.font.Font(None, min(self.cell_size) // 2)
                        text = font.render(str(self.grid[row][col]), True, self.BLACK)
                        text_rect = text.get_rect(center=(x + self.cell_size[0] // 2, y + self.cell_size[1] // 2))
                        self.win.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.win, self.GRAY, (x, y, self.cell_size[0], self.cell_size[1]))
                    if self.flags[row][col]:
                        pygame.draw.circle(self.win, self.RED,
                                           (x + min(self.cell_size) // 2, y + min(self.cell_size) // 2),
                                           min(self.cell_size) // 4)
                        
        menu_button_rect = pygame.Rect(210, 550, 180, 30)
        pygame.draw.rect(self.win, self.TEAL, menu_button_rect)
        menu_text = self.font.render("Menu", True, self.BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        self.win.blit(menu_text, menu_text_rect)
        
        restart_button_rect = pygame.Rect(230, 30, 140, 30)
        pygame.draw.rect(self.win, self.TEAL, restart_button_rect)
        restart_text = self.font.render("Restart", True, self.BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        self.win.blit(restart_text, restart_text_rect)

        for i in range(self.cols + 1):
            pygame.draw.line(self.win, self.BLACK,
                             (self.grid_top_left[0] + i * self.cell_size[0], self.grid_top_left[1]),
                             (self.grid_top_left[0] + i * self.cell_size[0], self.grid_top_left[1] + self.grid_size[1]))
        for i in range(self.rows + 1):
            pygame.draw.line(self.win, self.BLACK,
                             (self.grid_top_left[0], self.grid_top_left[1] + i * self.cell_size[1]),
                             (self.grid_top_left[0] + self.grid_size[0], self.grid_top_left[1] + i * self.cell_size[1]))
    
    def draw_menu(self):
        self.win.fill(self.WHITE)
        self.win.blit(self.background_image, (0, 0))

        if not self.in_settings_menu: 
            play_button_rect = pygame.Rect(200, 250, 200, 50)
            settings_button_rect = pygame.Rect(200, 325, 200, 50)
            quit_button_rect = pygame.Rect(200, 400, 200, 50)

            pygame.draw.rect(self.win, self.TEAL, play_button_rect)
            pygame.draw.rect(self.win, self.TEAL, settings_button_rect)
            pygame.draw.rect(self.win, self.TEAL, quit_button_rect)

            play_text = self.font.render("Play", True, self.BLACK)
            settings_text = self.font.render("Settings", True, self.BLACK)
            quit_text = self.font.render("Quit", True, self.BLACK)

            text_rect = play_text.get_rect(center=play_button_rect.center)
            self.win.blit(play_text, text_rect)

            text_rect = settings_text.get_rect(center=settings_button_rect.center)
            self.win.blit(settings_text, text_rect)

            text_rect = quit_text.get_rect(center=quit_button_rect.center)
            self.win.blit(quit_text, text_rect)
        else:  
            pygame.draw.rect(self.win, self.TEAL, (200, 200, 210, 50)) 
            slider_position = int((self.field_size_value - 8) / 12 * 200)
            pygame.draw.rect(self.win, self.RED, (200 + slider_position, 200, 10, 50))
            
            settings_title = self.settings_menu_font.render("Settings", True, self.WHITE)
            settings_title_rect = settings_title.get_rect(center=(self.window_size[0] // 2, 100))
            self.win.blit(settings_title, settings_title_rect)

            menu_button_rect = pygame.Rect(200, 450, 200, 50)
            pygame.draw.rect(self.win, self.TEAL, menu_button_rect)
            menu_text = self.settings_menu_font.render("Menu", True, self.BLACK)
            menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
            self.win.blit(menu_text, menu_text_rect)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = event.pos
                row = (y - self.grid_top_left[1]) // self.cell_size[1]
                col = (x - self.grid_top_left[0]) // self.cell_size[0]

                if event.button == 1:
                    x, y = event.pos
                    if self.in_settings_menu:
                        if 200 <= x <= 410 and 200 <= y <= 250:  
                            self.field_size_value = int((x - 200) / 200 * 12 + 8)
                            self.save_field_size_value()
                    if not self.in_settings_menu:  
                        play_button_rect = pygame.Rect(200, 250, 200, 50)
                        settings_button_rect = pygame.Rect(200, 325, 200, 50)
                        quit_button_rect = pygame.Rect(200, 400, 200, 50)
                        
                        if play_button_rect.collidepoint(x, y):
                            self.game_over = False
                            self.first_click = True
                            self.generate_mines()
                            return True
                        elif settings_button_rect.collidepoint(x, y):
                            self.in_settings_menu = True  
                        elif quit_button_rect.collidepoint(x, y):
                            pygame.quit()
                            quit()
                    else:  
                        menu_button_rect = pygame.Rect(200, 450, 200, 50)
                        if menu_button_rect.collidepoint(x, y):
                            self.in_settings_menu = False
        return False

    def run_game(self):
        in_menu = True
        running = True

        while running:
            if self.game_over:
                in_menu = True
                self.game_over = not(self.game_over)
                
            if in_menu:
                self.draw_menu()
                pygame.display.update()
                in_menu = not self.handle_menu_events()
                continue

            self.handle_events()

            if self.check_victory():
                print("You won!")
                self.game_over = True

            self.draw_grid()
            pygame.display.update()


            while in_menu:
                in_menu = self.handle_menu_events()
                pygame.time.Clock().tick(30)
    
if __name__ == "__main__":
    minesweeper = MinesweeperGame()
    minesweeper.run_game()