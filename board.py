import random
import pygame
from game_object import *
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




class Board:
    SIZE = 0
    width  =0
    height  =0
    matrix = SIZE * [0]
    for i in range(SIZE):
        matrix[i] = [0]*SIZE
    def __init__(self, size, width, height):
        self.width = width
        self.height = height
        self.SIZE = size;
        self.matrix = self.SIZE*[0]
        for i in range(self.SIZE):
            self.matrix[i] = [0] * self.SIZE
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.matrix[i][j] = random.randint(0, 4)

    def draw_init (self, screen):
        screen.fill(WHITE)
        for i in range(self.SIZE-1):
            pygame.draw.line(screen, BLACK, [(i+1)*self.width/self.SIZE,0],[(i+1)*self.width/self.SIZE,self.height])
            pygame.draw.line(screen, BLACK, [0,(i + 1) * self.height / self.SIZE], [self.width, (i + 1) * self.height / self.SIZE])

    def draw(self, screen):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                object = GameObject(round(self.width/(2*self.SIZE)+i*self.width/self.SIZE),round(self.height/(2*self.SIZE)+j*self.height/self.SIZE),round(0.9*self.width/(2*self.SIZE)),self.matrix[i][j])
                object.draw(screen)
    def getcoords(self, x, y):
        section_x = self.width/self.SIZE;
        section_y = self.width/self.SIZE;
        return (x//section_x,y//section_y)




