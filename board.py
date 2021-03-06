import random
import pygame.draw
from game_object import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (100, 0, 100)
YELLOW = (255, 128, 0)
LIGHT_BLUE = (130, 200, 255)

Colors = [RED, GREEN, BLUE, VIOLET, YELLOW]


class Board:
    SIZE = 0  # количество фишек на поле
    width = 0
    height = 0
    matrix_of_colors = [[0 for _ in range(SIZE)] for _ in range(SIZE)]  # хранит цвета
    candidates = []

    def __init__(self, size, width, height, top_hollow):
        self.width = width
        self.height = height
        self.SIZE = size
        self.matrix_of_colors = self.SIZE * [0]
        for i in range(self.SIZE):
            self.matrix_of_colors[i] = [0] * self.SIZE
        self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        while self.is_there_three_in_a_row():
            self.matrix_of_colors = [[random.choice(Colors) for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.top_hollow = top_hollow

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
        for i in range(self.SIZE):
            pygame.draw.line(screen, BLACK, [i * self.width / self.SIZE, self.top_hollow],
                             [i * self.width / self.SIZE, self.height])
            pygame.draw.line(screen, BLACK, [0, self.top_hollow + i * (self.height - self.top_hollow) / self.SIZE],
                             [self.width, self.top_hollow + i * (self.height - self.top_hollow) / self.SIZE])

    def draw(self, screen):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                obj = GameObject(round(self.width / (2 * self.SIZE) + i * self.width / self.SIZE),
                                 round(self.top_hollow + (self.height - self.top_hollow) / (2 * self.SIZE) + j * (self.height - self.top_hollow) / self.SIZE),
                                 round(0.9 * self.width / (2 * self.SIZE)),
                                 self.matrix_of_colors[i][j])
                obj.draw(screen)

    def draw_selected(self, screen, x, y):
        x_coord = round(x * self.width / self.SIZE)
        y_coord = round(self.top_hollow + y * (self.height - self.top_hollow) / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round((self.height - self.top_hollow) / self.SIZE)
        pygame.draw.rect(screen, LIGHT_BLUE, (x_coord + 1, y_coord + 1, w - 1, h - 1))

    def erase_selected(self, screen, x, y):
        x_coord = round(x * self.width / self.SIZE)
        y_coord = round(self.top_hollow + y * (self.height - self.top_hollow) / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round((self.height - self.top_hollow) / self.SIZE)
        pygame.draw.rect(screen, WHITE, (x_coord + 1, y_coord + 1, w - 1, h - 1))

    def get_coords(self, x, y):
        section_x = self.width / self.SIZE
        section_y = (self.height - self.top_hollow) / self.SIZE
        return x // section_x, (y - self.top_hollow) // section_y

    def goal(self, x, y, x2, y2):
        self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2] = \
            self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y]
        if self.is_there_three_in_a_row():
            return True
        else:
            self.matrix_of_colors[x2][y2], self.matrix_of_colors[x][y] = \
                self.matrix_of_colors[x][y], self.matrix_of_colors[x2][y2]
            return False

    def boom(self, screen):
        to_clear = self.where_to_clear()
        w = round(self.width / self.SIZE)
        h = round((self.height - self.top_hollow) / self.SIZE)
        for t in range(10):
            for j in range(self.SIZE):
                for i in range(self.SIZE):
                    if to_clear[i][j] == 1:
                        x = round(i * self.width / self.SIZE)
                        y = round(self.top_hollow + j * (self.height - self.top_hollow) / self.SIZE)
                        pygame.draw.rect(screen, WHITE, (x + 1, y + 1, w - 1, h - 1))
                        pygame.draw.circle(screen, self.matrix_of_colors[i][j],
                                           (x + self.width // (2 * self.SIZE), y + (self.height - self.top_hollow) // (2 * self.SIZE)),
                                           round(0.9 * self.width / (2 * self.SIZE) * (1 - (t + 1) / 10)))

            pygame.display.flip()
            pygame.time.wait(50)

        s = 0
        to_clear = self.where_to_clear()
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if to_clear[i][j] == 1:
                    self.matrix_of_colors[i][j] = WHITE
                    s += 1
        return s

    def fall(self, screen):
        w = round(self.width / self.SIZE)
        h = round((self.height - self.top_hollow) / self.SIZE)
        list_of_whites = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for j in range(self.SIZE):
            for i in range(self.SIZE):
                if self.matrix_of_colors[i][j] == WHITE:
                    list_of_whites[i][j] = 1
        cells_to_fall = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for i in range(self.SIZE):
            counter = 0
            # higher_than_whites = False
            highers = []
            for j in range(self.SIZE - 1, -1, -1):
                if list_of_whites[i][j] == 1:
                    counter += 1
                    # higher_than_whites = False
                if list_of_whites[i][j] == 0:
                    cells_to_fall[i][j] = counter
            # for j in highers:
            #     cells_to_fall[i][j] = counter

        for t in range(100):
            self.draw_init(screen)
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if list_of_whites[i][j] == 1 or cells_to_fall[i][j] > 0:
                        x = round(i * self.width / self.SIZE)
                        y = round(self.top_hollow + j * (self.height - self.top_hollow) / self.SIZE)
                        pygame.draw.rect(screen, WHITE, (x + 1, y + 1, w - 1, h - 1))
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if cells_to_fall[i][j] > 0:
                        x = round(i * self.width / self.SIZE)
                        y = round(self.top_hollow + j * (self.height - self.top_hollow) / self.SIZE)
                        pygame.draw.circle(screen, self.matrix_of_colors[i][j],
                                           (x + w // 2, round(y + w // 2 + w * cells_to_fall[i][j] * (t + 1) / 100)),
                                           round(0.9 * w // 2))
            pygame.display.flip()
            pygame.time.wait(3)

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
        y_coord1 = round(self.top_hollow + y1 * (self.height - self.top_hollow) / self.SIZE)
        x_coord2 = round(x2 * self.width / self.SIZE)
        y_coord2 = round(self.top_hollow + y2 * (self.height - self.top_hollow) / self.SIZE)
        w = round(self.width / self.SIZE)
        h = round((self.height - self.top_hollow) / self.SIZE)
        for i in range(100):
            self.draw_init(screen)
            pygame.draw.rect(screen, WHITE, (x_coord1 + 1, y_coord1 + 1, w - 1, h - 1))
            pygame.draw.rect(screen, WHITE, (x_coord2 + 1, y_coord2 + 1, w - 1, h - 1))
            pygame.draw.circle(screen, self.matrix_of_colors[x2][y2], (
                round(((99 - i) * x_coord1 + (1 + i) * x_coord2) / 100) + 25,
                round(((99 - i) * y_coord1 + (1 + i) * y_coord2) / 100) + 25), 22)
            pygame.draw.circle(screen, self.matrix_of_colors[x1][y1], (
                round(((1 + i) * x_coord1 + (99 - i) * x_coord2) / 100) + 25,
                round(((1 + i) * y_coord1 + (99 - i) * y_coord2) / 100) + 25), 22)
            pygame.display.flip()
            pygame.time.wait(5)
        self.draw_init(screen)


if __name__ == "__main__":
    print("This module is not for direct call!")
