# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from board import *
from game_object import *

WIDTH = 500
HEIGHT = 500
FPS = 30

SIZE = 10

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

board = Board(SIZE, WIDTH, HEIGHT)
board.draw_init(screen)
board.draw(screen)
# Цикл игры
running = True
selected = 0
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selected == 0:
                selected = 1
                (x, y) = board.getcoords(event.pos[0], event.pos[1])

            if selected == 1:
                (x2, y2) = board.getcoords(event.pos[0], event.pos[1])
                dist = abs(x-x2)+abs(y-y2)
                if dist == 1:
                    (board.matrix[int(x2)][int(y2)], board.matrix[int(x)][int(y)]) = (board.matrix[int(x)][int(y)],board.matrix[int(x2)][int(y2)])
                    selected = 0
                    board.draw(screen)
                else:
                    x = x2
                    y = y2

    # Обновление

    # Рендеринг
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()