import random
import pygame.draw
from game_object import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (80, 0, 80)
YELLOW = (255, 128, 0)
LIGHT_BLUE = (130, 200, 255)

Colors = [RED, GREEN, BLUE, VIOLET, YELLOW]


class Board:
    SIZE = 0  # количество фишек на поле
    width = 0
    height = 0
    matrix_of_colors = [[0 for _ in range(SIZE)] for _ in range(SIZE)]  # хранит цвета
    matrix_existence = SIZE * [0]  # хранит существование фишки для поиска соседей
    candidates = []
    group = 0

    def __init__(self, size, width, height):
        self.width = width
        self.height = height
        self.SIZE = size
        self.matrix_of_colors = self.SIZE * [0]
        self.matrix_existence = self.SIZE * [0]
        for i in range(self.SIZE):
            self.matrix_of_colors[i] = [0] * self.SIZE
            self.matrix_existence[i] = self.SIZE * [0]
        self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        while self.is_there_three_in_a_row():
            self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.matrix_existence = [[1 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def is_there_three_in_a_row(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE - 2):
                if self.matrix_of_colors[i][j] == self.matrix_of_colors[i][j + 1] == self.matrix_of_colors[i][j + 2] \
                        or self.matrix_of_colors[j][i] == self.matrix_of_colors[j + 1][i] == self.matrix_of_colors[j + 2][i]:
                    return True
        return False

    def draw_init(self, screen):
        screen.fill(WHITE)
        for i in range(self.SIZE - 1):
            pygame.draw.line(screen, BLACK, [(i + 1) * self.width / self.SIZE, 0],
                             [(i + 1) * self.width / self.SIZE, self.height])
            pygame.draw.line(screen, BLACK, [0, (i + 1) * self.height / self.SIZE],
                             [self.width, (i + 1) * self.height / self.SIZE])

    def draw(self, screen):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                obj = GameObject(round(self.width / (2 * self.SIZE) + i * self.width / self.SIZE),
                                 round(self.height / (2 * self.SIZE) + j * self.height / self.SIZE),
                                 round(0.9 * self.width / (2 * self.SIZE)),
                                 self.matrix_of_colors[i][j])
                obj.draw(screen)

    def draw_selected(self, screen, x, y):
        x_coord = round(x * self.width / self.SIZE)
        y_coord = round(y * self.height / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round(self.height / self.SIZE)
        pygame.draw.rect(screen, LIGHT_BLUE, (x_coord + 1, y_coord + 1, w - 1, h - 1))

    def erase_selected(self, screen, x, y):
        x_coord = round(x * self.width / self.SIZE)
        y_coord = round(y * self.height / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round(self.height / self.SIZE)
        pygame.draw.rect(screen, WHITE, (x_coord + 1, y_coord + 1, w - 1, h - 1))

    def getcoords(self, x, y):
        section_x = self.width / self.SIZE
        section_y = self.width / self.SIZE
        return x // section_x, y // section_y

    def goal(self, x, y, x2, y2):
        (self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2]) = (
            self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y])
        a = self.boom(x, y)
        b = self.boom(x2, y2)
        if a or b:
            return True
        else:
            (self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y]) = \
                (self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2])
            return False

    def boom(self, x, y):
        self.group = 1
        self.candidates.append((x, y))
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.matrix_existence[i][j] = 1
        self.look_all_neighbors(x, y, self.matrix_of_colors[x][y])
        if self.group >= 3:
            for i in self.candidates:
                self.matrix_of_colors[i[0]][i[1]] = WHITE
            self.candidates.clear()
            self.group = 1
            return True
        else:
            self.candidates.clear()
            self.group = 1
            return False

    def look_all_neighbors(self, x, y, color):
        self.matrix_existence[x][y] = 0
        if x != self.SIZE - 1:
            if self.matrix_of_colors[x + 1][y] == color and self.matrix_existence[x + 1][y] != 0:
                self.group += 1
                self.candidates.append((x + 1, y))

        if y != self.SIZE - 1:
            if self.matrix_of_colors[x][y + 1] == color and self.matrix_existence[x][y + 1] != 0:
                self.group += 1
                self.look_all_neighbors(x, y + 1, color)
                self.candidates.append((x, y + 1))

        if x != 0:
            if self.matrix_of_colors[x - 1][y] == color and self.matrix_existence[x - 1][y] != 0:
                self.group += 1
                self.look_all_neighbors(x - 1, y, color)
                self.candidates.append((x - 1, y))

        if y != 0:
            if self.matrix_of_colors[x][y - 1] == color and self.matrix_existence[x][y - 1] != 0:
                self.group += 1
                self.look_all_neighbors(x, y - 1, color)
                self.candidates.append((x, y - 1))
