import pygame
import random

pygame.init()
pygame.display.set_caption("Minesweeper")
size = (width, height) = pygame.display.Info().current_w, pygame.display.Info().current_h - 60
# size = (1200, 600)
screen = pygame.display.set_mode(size)

# Work with Music!!

# IF YOU NEED TO STOP THE MUSIC, USE: pygame.mixer.music.stop()

# ALSO THIS pygame.mixer.music.set_volume()  - VOLUME ADJUST

pygame.mixer.music.set_volume(0.8)
previous_composition = "starting..."

def music_player(composition_name):
    global previous_composition

    if (composition_name != previous_composition):
        previous_composition = composition_name
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(composition_name)
            pygame.mixer.music.play(-1)
        except:
            pass


def get_level_value(level):  # GETTING LEVEL NUMBERS KEYS!!!!!!!!!
    level_values = {
        'playlevel_1': 1,
        'playlevel_2': 2,
        'playlevel_3': 3,
        'playlevel_4': 4,
        'playlevel_5': 5,
        'playlevel_6': 6,
        'playlevel_7': 7,
        'playlevel_8': 8,
        'playlevel_9': 9,
        'playlevel_10': 10
    }

    return level_values.get(level, None)


def title(font_value, string, color, x, y):
    font = pygame.font.Font(None, int(font_value))
    text = font.render(str(string), True,
                       color)
    text_rect = text.get_rect(center=(x, y))
    return text, text_rect


def load_image(image):
    try:
        return pygame.image.load(image)
    except:
        return None


def load():
    try:
        with open("storage.txt", "r") as file:
            return file.readlines()
    except:
        pass


def save(field_size_value):                                     #  FIX LATER!!!!
    with open("storage.txt", "w") as file:
        file.write(str(field_size_value))


class Menu:
    def __init__(self, size1):
        self.square_size = 80  # for squares
        
        # LOADING SPRITE (DO TRY - EXCEPT LATER!! AND ALSO DO IT IN A FUNCTION (METHOD) !!)
        self.mine_image = pygame.image.load('mine.png').convert_alpha()
        self.mine_image = pygame.transform.scale(self.mine_image, (self.square_size, self.square_size))  # Resizing the sprite image
        
        """
        # CREATING MASKS TO DO THE TRANSPARENCY:
        mask_white = self.mine_image.copy()
        mask_white.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT) # - KILLING WHITE COLOR                               # OLD METHOD!!!!!! - DELETE LATER!! (NOW ALL ABOUT SPRITES IS OK)
        mask_gray = self.mine_image.copy()
        mask_gray.fill((239, 238, 238, 255), None, pygame.BLEND_RGBA_MULT) # - KILLING GREY COLOR
        
        # COMBINING MASKS:
        combined_mask = pygame.mask.from_surface(mask_white)
        combined_mask.draw(mask_gray, (0, 0), None, pygame.BLEND_RGBA_MULT)
        
        self.mine_image.blit(self.mine_image, (0, 0), combined_mask) # - USING MASK
        """
            
        self.level_rects = []  # for level rects (positions in level selection menu)
        self.squares = []
        self.color_squares = [(255, 255, 255), (255, 0, 0), (0, 255, 0),
                              (0, 0, 255), (150, 150, 150),
                              (195, 195, 195), (0, 128, 128), (128, 0, 128),
                              (255, 127, 0), (255, 255, 0), (64, 224, 208)]

        self.window_size = size1

        self.win = pygame.display.set_mode(self.window_size)

        self.field_size_value = 10
        self.field2_size_value = 10
        self.field3_size_value = 10
        
        self.game_over = False

        self.colors = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255),
                       "RED": (255, 0, 0), "GREEN": (0, 255, 0),
                       "BLUE": (0, 0, 255), "GRAY": (150, 150, 150),
                       "LIGHT_GRAY": (100, 100, 100), "TEAL": (0, 128, 128),
                       "PURPLE": (128, 0, 128), "LIGHT_BLUE": (0, 191, 255),
                       "YELLOW": (255, 255, 0), "ORANGE": (255, 127, 0),
                       "MYRTLE": (33, 66, 30), "LIGHT_TURQUOISE": (64, 224, 208)}
        self.color_digit = ["LIGHT_TURQUOISE", "GREEN", "LIGHT_BLUE", "PURPLE",
                            "BLUE", "YELLOW", "MYRTLE", "ORANGE", "RED", "BLACK"]

        self.background_image = pygame.transform.scale(load_image("background.jpg").convert(), self.window_size)
        self.background_p_image = pygame.transform.scale(load_image("background_p3.jpg").convert(), self.window_size)

        self.title_size = (self.window_size[0] * 0.75, self.window_size[1] * 0.16)
        self.title_image = pygame.transform.scale(load_image("title.png").convert_alpha(),
                                                  (self.title_size[0], self.title_size[1]))
        self.resume_image = load_image("resume.png").convert_alpha()
        self.start_image = load_image("start.png").convert_alpha()
        self.settings_image = load_image("settings.png").convert_alpha()
        self.end_image = load_image("end.png").convert_alpha()

        self.resume_size = self.resume_image.get_rect().bottomright
        self.start_size = self.start_image.get_rect().bottomright
        self.settings_size = self.settings_image.get_rect().bottomright
        self.end_size = self.end_image.get_rect().bottomright

        self.title_place = ((self.window_size[0] * 0.25) / 2, 50)
        self.resume_place = ((self.window_size[0] - self.resume_size[0]) / 2,
                             self.title_place[1] + self.title_size[1] + 50)
        self.start_place = ((self.window_size[0] - self.start_size[0]) / 2,
                            self.resume_place[1] + + self.resume_size[1] + 30)
        self.settings_place = ((self.window_size[0] - self.settings_size[0]) / 2,
                               self.start_place[1] + self.start_size[1] + 30)
        self.end_place = ((self.window_size[0] - self.end_size[0]) / 2,
                          self.settings_place[1] + self.settings_size[1] + 30)

        self.description = ["Количество мин: 6nРазмер поля: 8x8nМесто: полигон",
                            "Количество мин: 8nРазмер поля: 8x8nМесто: лес",
                            "Количество мин: 10nРазмер поля: 10x10nМесто: лес",
                            "Количество мин: 16nРазмер поля: 12x12nМесто: лес",
                            "Количество мин: 5nРазмер поля: 20x20nМесто: лес",
                            "Количество мин: 15nРазмер поля: 10x10nМесто: лес",
                            "Количество мин: 30nРазмер поля: 15x15nМесто: тайга",
                            "Количество мин: 28nРазмер поля: 14x14nМесто: лес",
                            "Количество мин: 100nРазмер поля: 20x20nМесто: лес",
                            "Количество мин: 389nРазмер поля: 20x20nМесто: лес"]
        self.levels_number = ["Обучение", "Уровень 1", "Уровень 2", "Уровень 3", "Уровень 4",
                              "Уровень 5", "Уровень 6", "Уровень 7", "Уровень 8", "Уровень 9"]
        self.font_value = 36
        self.font = pygame.font.Font(None, self.font_value)

        self.settings_menu_font = pygame.font.Font(None, 42)
        self.in_settings_menu = False

    def draw_level_selection(self):
        music_player('elevator.mp3')

        self.win.fill(self.colors["WHITE"])
        self.win.blit(self.background_p_image, (0, 0))
        text_center_y = self.font_value / 4 * 3 + 4

        text = title(100, "Задания", self.colors["BLACK"],
                     (self.window_size[0] - 28) // 2, text_center_y)
        self.win.blit(*text)

        levels_size = ((self.window_size[0] - 28) / 6, (self.window_size[1] - text[1].bottom - 9) / 5)
        between_levels_size = (levels_size[0] / 6, levels_size[1])
        x, y = between_levels_size[0], 10
        x += 11
        y += text[1].bottom + 50
        n = 0

        for level_number in range(10):
            if len(self.level_rects) < 10:
                level_rect = pygame.Rect(x, y, levels_size[0], levels_size[1])
                self.level_rects.append(level_rect)

            pygame.draw.rect(self.win, self.colors["WHITE"], (x, y, levels_size[0], levels_size[1]))
            pygame.draw.rect(self.win, self.colors["LIGHT_GRAY"], (x, y, levels_size[0], levels_size[1]), 4)
            pygame.draw.rect(self.win, self.colors["GRAY"], (x, y, levels_size[1] * 0.75, levels_size[1]))
            pygame.draw.rect(self.win, self.colors["LIGHT_GRAY"], (x, y, levels_size[0], levels_size[1]), 4)

            text1 = title(int(levels_size[1]), str(level_number), self.colors[self.color_digit[level_number]],
                          x + (levels_size[1] * 0.75) // 2, y + levels_size[1] // 2)
            self.win.blit(*text1)

            center_y = y + levels_size[1] // 6

            for string in self.description[level_number].split("n"):
                text2 = title(int(levels_size[0] // 14), string, self.colors["BLACK"],
                              x + (levels_size[0] + levels_size[1] * 0.75) // 2, center_y)
                self.win.blit(*text2)
                center_y += levels_size[1] // 3

            text3 = title(int(levels_size[0] // 6), self.levels_number[level_number], self.colors["BLACK"],
                          x + (levels_size[0]) // 2, y + levels_size[1] + 15)
            self.win.blit(*text3)

            x += between_levels_size[0] + levels_size[0]
            if x == (self.window_size[0] - 17):
                x = between_levels_size[0] + 11
                y += between_levels_size[1] + levels_size[1]
                n += 1

        menu_button_rect = pygame.Rect(678, 770, 180, 30)
        pygame.draw.rect(self.win, self.colors["TEAL"], menu_button_rect)
        menu_text = self.font.render("Menu", True, self.colors["BLACK"])
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        self.win.blit(menu_text, menu_text_rect)

    def draw_menu(self):
        self.win.fill(self.colors["WHITE"])
        self.win.blit(self.background_image, (0, 0))
        if not self.in_settings_menu:
            self.win.blit(self.title_image, self.title_place)
            self.win.blit(self.resume_image, self.resume_place)
            self.win.blit(self.start_image, self.start_place)
            self.win.blit(self.settings_image, self.settings_place)
            self.win.blit(self.end_image, self.end_place)

        else:
            pygame.draw.rect(self.win, self.colors["TEAL"], (665, 250, 210, 50))               # SLIDER ABOUT GRID SIZE
            slider_position = int((self.field_size_value - 8) / 12 * 200)
            pygame.draw.rect(self.win, self.colors["RED"], (665 + slider_position, 250, 10, 50))
            
            pygame.draw.rect(self.win, self.colors["TEAL"], (665, 380, 210, 50))                # SLIDER ABOUT MINES COUNT
            slider2_position = int((self.field2_size_value - 8) / 12 * 200)
            pygame.draw.rect(self.win, self.colors["RED"], (665 + slider2_position, 380, 10, 50))
            
            pygame.draw.rect(self.win, self.colors["TEAL"], (665, 510, 210, 50))                # SLIDER ABOUT VOLUME
            slider3_position = int((self.field3_size_value - 8) / 12 * 200)
            pygame.draw.rect(self.win, self.colors["RED"], (665 + slider3_position, 510, 10, 50))

            settings_title = self.settings_menu_font.render("Settings", True, self.colors["BLACK"])
            settings_title_rect = settings_title.get_rect(center=(770, 100))
            self.win.blit(settings_title, settings_title_rect)

            mines_title = self.settings_menu_font.render("8        field      20", True, self.colors["BLACK"])  # SUBTEXT FOR GRID SIZE SLIDER
            mines_title_rect = mines_title.get_rect(center=(773, 320))
            self.win.blit(mines_title, mines_title_rect)
            
            volume_title = self.settings_menu_font.render("0      mines     1", True, self.colors["BLACK"])    # SUBTEXT FOR MINE COUNT SLIDER
            volume_title_rect = volume_title.get_rect(center=(770, 450))
            self.win.blit(volume_title, volume_title_rect)

            volume_title = self.settings_menu_font.render("0      volume     1", True, self.colors["BLACK"])    # SUBTEXT FOR VOLUME SLIDER
            volume_title_rect = volume_title.get_rect(center=(770, 580))
            self.win.blit(volume_title, volume_title_rect)

            menu_button_rect = pygame.Rect(665, 750, 210, 50)                                    # MENU BUTTON
            pygame.draw.rect(self.win, self.colors["TEAL"], menu_button_rect)
            menu_text = self.settings_menu_font.render("Menu", True, self.colors["BLACK"])
            menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
            self.win.blit(menu_text, menu_text_rect)
            
            reset_button_rect = pygame.Rect(625, 650, 290, 50)                                    # NEW RESET BUTTON (NEEDS LOGIC FROM @MINITS)
            pygame.draw.rect(self.win, self.colors["LIGHT_TURQUOISE"], reset_button_rect)
            reset_text = self.settings_menu_font.render("Reset progress", True, self.colors["BLACK"])
            reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
            self.win.blit(reset_text, reset_text_rect)

    def setting_events(self, x, y):
        if 665 <= x <= 875 and 250 <= y <= 300:                               # THIS IS FOR GRID SIZE SLIDER LOGIC
            self.field_size_value = int((x - 665) / 200 * 12 + 8)
            #save(self.field_size_value)
        elif 665 <= x <= 875 and 510 <= y <= 560:                                #THIS IS FOR VOLUME SLIDER LOGIC
            self.field3_size_value = int((x - 665) / 200 * 12 + 8)
            slider_value = (x - 665) / 210
            pygame.mixer.music.set_volume(slider_value)
            # NEED TO SAVE VOLUME VALUE TOO!
        elif 665 <= x <= 875 and 380 <= y <= 430:                              # THIS IS FOR MINES COUNT LOGIC FOR TRAINING GAME 
            self.field2_size_value = int((x - 665) / 200 * 12 + 8)
            slider_mines_value = (x - 665) / 210
            mines_count = int(slider_mines_value * (((minesweeper.rows * minesweeper.cols) / 2) - 5) + 5)
            if mines_count < 5:
                mines_count = 5
            elif mines_count > ((minesweeper.rows * minesweeper.cols) / 2):                                   # THIS IS NOT TO EXCEED HALF OF ALL THE CELLS IN MINES (UNREAL TO COMPLETE OTHERWISE)
                mines_count = ((minesweeper.rows * minesweeper.cols) / 2)
            print(mines_count)           # DELETE THIS PRINT LATER!! THIS IS TO SHOW HOW FINE IT WORKS!
            
        reset_button_rect = pygame.Rect(625, 650, 290, 50)           # IF RESET BUTTON IS TRIGGERED! -> Do something (erase progress...)
        if reset_button_rect.collidepoint(x, y):
            # ADD LOGIC HERE @MINITS ( -> TOKAREV WINS)
            pass

        menu_button_rect = pygame.Rect(665, 750, 210, 50)
        if menu_button_rect.collidepoint(x, y):
            return False
        return True

    def handle_menu_events(self):
        x, y = event.pos
        if event.button == 1:
            if self.in_settings_menu:
                self.in_settings_menu = self.setting_events(x, y)
            if not self.in_settings_menu:
                play_button_rect = pygame.Rect(*self.resume_place, self.resume_size[0] - 2, self.resume_size[1] - 2)
                new_play_button_rect = pygame.Rect(*self.start_place, self.start_size[0] - 2, self.start_size[1] - 2)
                settings_button_rect = pygame.Rect(*self.settings_place, self.settings_size[0] - 2,
                                                   self.settings_size[1] - 2)
                quit_button_rect = pygame.Rect(*self.end_place, self.end_size[0] - 2, self.end_size[1] - 2)

                if new_play_button_rect.collidepoint(x, y):
                    return "play"
                elif play_button_rect.collidepoint(x, y):
                    return "levels"
                elif settings_button_rect.collidepoint(x, y):
                    self.in_settings_menu = True
                elif quit_button_rect.collidepoint(x, y):
                    return "quit"

        return "menu"

    def create_square(self, x, y):  # Creating squares on X and Y
        speed_x = random.choice([-2, -1, 1, 2])
        speed_y = random.choice([-2, -1, 1, 2])

        square = {
            'rect': pygame.Rect(x, y, self.square_size, self.square_size),
            'speed': [speed_x, speed_y],
            'collided': False,
            'collides': 0
        }
        self.squares.append(square)

    def update_squares(self):
        for square in self.squares:
            square['rect'].move_ip(square['speed'][0], square['speed'][1])

            if square['rect'].left < 0 or square['rect'].right > self.win.get_width():
                square['speed'][0] *= -1
                square['collides'] += 1
            if square['rect'].top < 0 or square['rect'].bottom > self.win.get_height():
                square['speed'][1] *= -1
                square['collides'] += 1

        self.check_collisions()
        self.draw_sprite()

    def check_collisions(self):
        squares_to_remove = []  # list for keeping "stuck" squares

        for i, square in enumerate(self.squares):
            for j, other_square in enumerate(self.squares):
                if i != j and not square['collided'] and not other_square['collided']:
                    if square['rect'].colliderect(other_square['rect']):
                        square['speed'][0] *= -1
                        square['speed'][1] *= -1
                        other_square['speed'][0] *= -1
                        other_square['speed'][1] *= -1
                        square['collided'] = True
                        square['collides'] += 1
                        other_square['collided'] = True
                        other_square['collides'] += 1

                if square['collides'] >= 100:  # after 100 hits
                    squares_to_remove.append(i)

                if other_square['collides'] >= 100:  # after 100 hits
                    squares_to_remove.append(j)

                square['collided'] = False

        # killing squares if need to
        unique_indexes_to_remove = set(squares_to_remove)
        for index in sorted(unique_indexes_to_remove, reverse=True):
            if 0 <= index < len(self.squares):
                self.squares.pop(index)

    def draw_sprite(self):
        for square in self.squares:  # drawing sprite
            self.win.blit(self.mine_image, square['rect'])

    """def draw_squares(self):                                 # GARBAGE NOW!!! - DELETE LATER!
        for square in self.squares:  # drawing squares
            pygame.draw.rect(self.win, square['color'], square['rect'])"""

    def draw_endscreen(self):  # added endscreen
        music_player('won.mp3')

        self.win.fill(self.colors["WHITE"])
        self.win.blit(self.background_image, (0, 0))

        menu_button_rect = pygame.Rect(678, 830, 180, 30)
        pygame.draw.rect(self.win, self.colors["TEAL"], menu_button_rect)
        menu_text = self.font.render("Menu", True, self.colors["BLACK"])
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        self.win.blit(menu_text, menu_text_rect)

        restart_button_rect = pygame.Rect(698, 40, 140, 30)
        pygame.draw.rect(self.win, self.colors["TEAL"], restart_button_rect)
        restart_text = self.font.render("Restart", True, self.colors["BLACK"])
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        self.win.blit(restart_text, restart_text_rect)

        font = pygame.font.Font(None, 90)
        text_surface = font.render("Level completed!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(size[0] // 2, size[1] // 2))
        self.win.blit(text_surface, text_rect)

        if len(self.squares) > 10:  # killing squares population
            self.squares.pop(0)

        self.update_squares()

    def handle_endscreen_events(self):  # extra handler for handling endscreen events.
        x, y = event.pos
        if 830 <= y <= 860 and 678 <= x <= 858:
            self.squares.clear()  # clearing array of squares
            return "menu"
        if 40 <= y <= 70 and 698 <= x <= 838:
            self.squares.clear()
            return "play"
        else:
            self.create_square(x, y)
        return "endscreen"

    def handle_draw_level_events(
            self):  # HANDLING DRAW_LEVELS AND RETURNING f"playlevel_{index} AS CONDITION TO START A LEVEL WITH A CERTAIN QUANTITY OF MINES AND TILES (CELLS)
        x, y = event.pos

        if 770 <= y <= 800 and 678 <= x <= 858:
            return "menu"

        for index, level_rect in enumerate(self.level_rects, start=1):
            if level_rect.collidepoint(x, y):
                return f"playlevel_{index}"

        return "levels"


class MinesweeperGame:
    def __init__(self, size1, flag):
        self.flag = flag
        self.window_size = size1
        self.grid_size = (min(int(self.window_size[0] * 0.8), int(self.window_size[1] * 0.8)),
                          min(int(self.window_size[0] * 0.8), int(self.window_size[1] * 0.8)))
        self.field_size = self.rows, self.cols = (10, 10)
        self.cell_size = (self.grid_size[0] // self.cols, self.grid_size[1] // self.rows)
        self.grid_top_left = ((self.window_size[0] - self.grid_size[0]) / 2,
                              (self.window_size[1] - self.grid_size[1]) / 2)
        self.colors = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255),
                       "RED": (255, 0, 0), "GREEN": (0, 255, 0),
                       "BLUE": (0, 0, 255), "GRAY": (150, 150, 150),
                       "LIGHT_GRAY": (100, 100, 100), "TEAL": (0, 128, 128),
                       "PURPLE": (128, 0, 128), "LIGHT_BLUE": (0, 191, 255),
                       "YELLOW": (255, 255, 0), "ORANGE": (255, 127, 0),
                       "MYRTLE": (33, 66, 30), "LIGHT_TURQUOISE": (64, 224, 208)}
        self.color_digit = ["LIGHT_TURQUOISE", "GREEN", "LIGHT_BLUE", "PURPLE",
                            "BLUE", "YELLOW", "MYRTLE", "ORANGE", "RED"]
        self.win = pygame.display.set_mode(self.window_size)

        self.game_over = False
        self.first_click = True

        self.mine_count = 2
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        self.background_image = pygame.transform.scale(load_image("background_p3.jpg").convert(), self.window_size)
        self.field_size_value = 10

        # self.field_size_value = load()
        self.field_size = self.rows, self.cols = (self.field_size_value, self.field_size_value)

        self.font = pygame.font.Font(None, 36)
        if self.flag:
            self.levels()
        else:
            self.generate_mines()

        self.determinant_of_mines()

    def levels(self):
        lines = load()[self.flag-1].split()
        li = len(lines)

        self.rows, self.cols = int(li ** 0.5), int(li ** 0.5)
        self.cell_size = (self.grid_size[0] // self.cols, self.grid_size[1] // self.rows)
        self.field_size = self.rows, self.cols
        self.field_size_value = self.cols
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.first_click = False

        n = 0
        for index1 in range(self.rows):
            for index2 in range(self.cols):
                if lines[n][0] == "-":
                    self.grid[index1][index2] = int(lines[n][0] + lines[n][1])
                    self.revealed[index1][index2] = int(lines[n][2])
                    self.flags[index1][index2] = int(lines[n][3])
                else:
                    self.grid[index1][index2] = int(lines[n][0])
                    self.revealed[index1][index2] = int(lines[n][1])
                    self.flags[index1][index2] = int(lines[n][2])
                n += 1


    def calculate_grid_position(self):
        self.grid_top_left = ((self.window_size[0] - self.grid_size[0]) // 2,
                              (self.window_size[1] - self.grid_size[1]) // 2)

    def generate_mines(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        mines = random.sample(range(self.rows * self.cols), self.mine_count)
        for position in mines:
            row = position // self.cols
            col = position % self.cols
            self.grid[row][col] = -1

    def determinant_of_mines(self):

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

        x, y = event.pos
        if 830 <= y <= 860 and 678 <= x <= 858:
            return "menu"
        if 40 <= y <= 70 and 698 <= x <= 838:
            self.first_click = True
            self.levels()
            self.determinant_of_mines()
            return "play"
        row = (y - self.grid_top_left[1]) // self.cell_size[1]
        col = (x - self.grid_top_left[0]) // self.cell_size[0]
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return "play"
        if event.button == 1 and not self.flags[row][col]:
            if self.first_click:
                while self.grid[row][col] != 0 or self.grid[row][col] == -1:
                    self.generate_mines()
                    self.determinant_of_mines()
                self.reveal_adjacent_safe_cells(row, col)
                self.first_click = False
                return "play"

            if self.grid[row][col] == -1:
                return "endscreen"
                #self.revealed = [[True for _ in range(self.cols)] for _ in range(self.rows)]
            else:
                if self.grid[row][col] == 0:
                    self.reveal_adjacent_safe_cells(row, col)
                self.revealed[row][col] = True
        elif event.button == 3 and not self.revealed[row][col]:
            self.flags[row][col] = not self.flags[row][col]

        return "play"

    def draw_grid(self):
        music_player('game.mp3')

        self.win.fill(self.colors["WHITE"])
        self.win.blit(self.background_image, (0, 0))

        self.cell_size = (self.grid_size[0] // self.field_size_value, self.grid_size[1] // self.field_size_value)
        self.calculate_grid_position()

        for row in range(self.rows):
            for col in range(self.cols):
                x = self.grid_top_left[0] + col * self.cell_size[0]
                y = self.grid_top_left[1] + row * self.cell_size[1]

                if self.revealed[row][col]:

                    pygame.draw.rect(self.win, self.colors["GRAY"], (x, y, self.cell_size[0], self.cell_size[1]))
                    if self.grid[row][col] == -1:
                        pygame.draw.circle(self.win, self.colors["BLACK"],
                                           (x + min(self.cell_size) // 2, y + min(self.cell_size) // 2),
                                           min(self.cell_size) // 4)
                    elif self.grid[row][col] == 0:
                        pass
                    else:
                        font = pygame.font.Font(None, min(self.cell_size))
                        text = font.render(str(self.grid[row][col]), True,
                                           self.colors[self.color_digit[self.grid[row][col] - 1]])
                        text_rect = text.get_rect(center=(x + self.cell_size[0] // 2, y + self.cell_size[1] // 2))
                        self.win.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.win, self.colors["LIGHT_GRAY"], (x, y, self.cell_size[0], self.cell_size[1]))
                    pygame.draw.rect(self.win, self.colors["GRAY"], (x, y, self.cell_size[0], self.cell_size[1]), 1)
                    if self.flags[row][col]:
                        pygame.draw.circle(self.win, self.colors["RED"],
                                           (x + min(self.cell_size) // 2, y + min(self.cell_size) // 2),
                                           min(self.cell_size) // 4)

        menu_button_rect = pygame.Rect(678, 830, 180, 30)
        pygame.draw.rect(self.win, self.colors["TEAL"], menu_button_rect)
        menu_text = self.font.render("Menu", True, self.colors["BLACK"])
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        self.win.blit(menu_text, menu_text_rect)

        restart_button_rect = pygame.Rect(698, 40, 140, 30)
        pygame.draw.rect(self.win, self.colors["TEAL"], restart_button_rect)
        restart_text = self.font.render("Restart", True, self.colors["BLACK"])
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        self.win.blit(restart_text, restart_text_rect)

        for i in range(self.cols + 1):
            pygame.draw.line(self.win, self.colors["BLACK"],
                             (self.grid_top_left[0] + i * self.cell_size[0], self.grid_top_left[1]),
                             (self.grid_top_left[0] + i * self.cell_size[0], self.grid_top_left[1] + self.grid_size[1]))
        for i in range(self.rows + 1):
            pygame.draw.line(self.win, self.colors["BLACK"],
                             (self.grid_top_left[0], self.grid_top_left[1] + i * self.cell_size[1]),
                             (self.grid_top_left[0] + self.grid_size[0], self.grid_top_left[1] + i * self.cell_size[1]))


if __name__ == "__main__":
    menu = Menu(size)
    running = True
    new_grid = True
    condition = "menu"
    minesweeper = MinesweeperGame(size, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if condition == "menu":
                    condition = menu.handle_menu_events()
                elif condition == "play":
                    condition = minesweeper.handle_events()
                elif condition == "endscreen":  # added check for endscreen
                    condition = menu.handle_endscreen_events()
                    new_grid = False
                elif condition == "levels":
                    condition = menu.handle_draw_level_events()

        if condition == "quit":
            running = False
            continue
        elif condition == "menu":
            menu.draw_menu()
            pygame.display.update()
            new_grid = True
        elif condition == "levels":
            menu.draw_level_selection()
            pygame.display.update()
            new_grid = False
        elif condition == "endscreen":  # endscreen condition
            menu.draw_endscreen()
            pygame.display.update()
        elif condition == "play":
            if new_grid:
                new_grid = False
                minesweeper = MinesweeperGame(size, 0)
            minesweeper.draw_grid()
            pygame.display.update()
            if minesweeper.check_victory():  # endscreen check
               condition = "endscreen"
        else:  # MANAGING CONDITION TO GET KEY (KEY = LEVEL_NUMBER)
            key = get_level_value(condition)
            minesweeper = MinesweeperGame(size,int(key))
            condition = "play"