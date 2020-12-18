import pygame


class GameObject:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

if __name__ == "__main__":
    print("This module is not for direct call!")
