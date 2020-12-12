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
selected = False
x_selected, y_selected = None, None
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод события
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                selected = True
                (x_selected, y_selected) = board.getcoords(event.pos[0], event.pos[1])
                board.draw_selected(screen, x_selected, y_selected)
            else:
                board.erase_selected(screen, x_selected, y_selected)
                (x2, y2) = board.getcoords(event.pos[0], event.pos[1])
                dist = abs(x_selected - x2) + abs(y_selected - y2)
                if dist == 1:
                    if board.goal(round(x_selected), round(y_selected), round(x2), round(y2)):
                        board.draw(screen)
                        selected = False
                    else:
                        x_selected = x2
                        y_selected = y2
                        board.draw_selected(screen, x_selected, y_selected)
                else:
                    x_selected = x2
                    y_selected = y2
                    board.draw_selected(screen, x_selected, y_selected)
            board.draw(screen)

    # Обновление

    # Рендеринг
    # После отрисовки всего обновляем экран
    pygame.display.flip()

pygame.quit()
