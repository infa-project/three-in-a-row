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

board = Board()
board.draw(screen, WIDTH, HEIGHT)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление

    # Рендеринг
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()