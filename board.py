import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = 10


class Board:
    matrix = SIZE*[0]
    for i in range(SIZE):
        matrix[i] = [0]*SIZE
    def __init__(self):
        for i in range(SIZE):
            for j in range(SIZE):
                self.matrix[i][j] = random.randint(0, 5)

    def draw (self, screen,width, height):
        screen.fill(WHITE)
        for i in range(SIZE-1):
            pygame.draw.line(screen,BLACK, [(i+1)*width/SIZE,0],[(i+1)*width/SIZE,height])
            pygame.draw.line(screen, BLACK, [0,(i + 1) * height / SIZE], [width, (i + 1) * height / SIZE])




