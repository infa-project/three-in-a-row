
import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (80, 0, 80)
YELLOW = (255, 128, 0)

Colors = [RED,GREEN, BLUE, VIOLET, YELLOW]

class GameObject:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = Colors[color]
    def draw(self, screen):
        pygame.draw.circle(screen, self.color,( self.x, self.y), self.r)





