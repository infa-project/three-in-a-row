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
    candidates = []

    def __init__(self, size, width, height):
        self.width = width
        self.height = height
        self.SIZE = size
        self.matrix_of_colors = self.SIZE * [0]
        for i in range(self.SIZE):
            self.matrix_of_colors[i] = [0] * self.SIZE
        self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        while self.is_there_three_in_a_row():
            self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def is_there_three_in_a_row(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE - 2):
                if (self.matrix_of_colors[i][j] != WHITE and
                    self.matrix_of_colors[i][j] == self.matrix_of_colors[i][j + 1] == self.matrix_of_colors[i][
                        j + 2]) or (self.matrix_of_colors[j][i] != WHITE and self.matrix_of_colors[j][i] ==
                                    self.matrix_of_colors[j + 1][i] == self.matrix_of_colors[j + 2][i]):
                    return True
        return False

    def where_to_clear(self):
        objects_to_clear = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for i in range(self.SIZE):
            for j in range(self.SIZE - 2):
                if self.matrix_of_colors[i][j] == self.matrix_of_colors[i][j + 1] == self.matrix_of_colors[i][j + 2]:
                    objects_to_clear[i][j] = objects_to_clear[i][j + 1] = objects_to_clear[i][j + 2] = 1
                if self.matrix_of_colors[j][i] == self.matrix_of_colors[j + 1][i] == self.matrix_of_colors[j + 2][i]:
                    objects_to_clear[j][i] = objects_to_clear[j + 1][i] = objects_to_clear[j + 2][i] = 1
        return objects_to_clear

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

    def get_coords(self, x, y):
        section_x = self.width / self.SIZE
        section_y = self.width / self.SIZE
        return x // section_x, y // section_y

    def goal(self, x, y, x2, y2):
        self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2] = \
            self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y]
        if self.is_there_three_in_a_row():
            return True
        else:
            self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y] = \
                self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2]
            return False

    def boom(self):
        to_clear = self.where_to_clear()
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if to_clear[i][j] == 1:
                    self.matrix_of_colors[i][j] = WHITE

    def fall(self):
        for _ in range(self.SIZE):
            for i in range(self.SIZE):
                for j in range(1, self.SIZE):
                    if self.matrix_of_colors[i][j] == WHITE:
                        self.matrix_of_colors[i][j], self.matrix_of_colors[i][j - 1] = \
                            self.matrix_of_colors[i][j - 1], self.matrix_of_colors[i][j]

    def fill(self):
        whites = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.matrix_of_colors[i][j] == WHITE:
                    whites.append((i, j))
        for coord in whites:
            self.matrix_of_colors[coord[0]][coord[1]] = random.choice(Colors)
        while self.is_there_three_in_a_row():
            for coord in whites:
                self.matrix_of_colors[coord[0]][coord[1]] = random.choice(Colors)
               
            
    def swap(self, screen, x1, y1, x2, y2):
        x_coord1 = round(x1 * self.width / self.SIZE)
        y_coord1 = round(y1 * self.height / self.SIZE)
        x_coord2 = round(x2 * self.width / self.SIZE)
        y_coord2 = round(y2 * self.height / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round(self.height / self.SIZE)
        for i in range(10):
            pygame.draw.rect(screen, WHITE, (x_coord1 + 1, y_coord1 + 1, w - 1, h - 1))
            pygame.draw.rect(screen, WHITE, (x_coord2 + 1, y_coord2 + 1, w - 1, h - 1))
            pygame.draw.circle(screen, self.matrix_of_colors[x2][y2], (round(((9-i)*x_coord1 + (1+i)*x_coord2)/10) + 25, round(((9-i)*y_coord1 + (1+i)*y_coord2)/10) + 25), 22)
            pygame.draw.circle(screen, self.matrix_of_colors[x1][y1], (round(((1+i)*x_coord1 + (9-i)*x_coord2)/10) + 25, round(((1+i)*y_coord1 + (9-i)*y_coord2)/10) + 25), 22)
            pygame.display.flip()
            pygame.time.wait(100)
        
        
if __name__ == "__main__":
    print("This module is not for direct call!")
