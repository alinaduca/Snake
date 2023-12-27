import pygame
import random
from pygame.math import Vector2


class Fruit:
    def __init__(self, cell_number):
        self.max_pos = cell_number - 1
        self.randomize()

    def draw(self, size, surface):
        fruit_rectangle = pygame.Rect(int(self.pos.x * size), int(self.pos.y * size), size, size)
        pygame.draw.rect(surface, (126, 166, 114), fruit_rectangle)

    def randomize(self):
        self.x = random.randint(0, self.max_pos)
        self.y = random.randint(0, self.max_pos)
        self.pos = Vector2(self.x, self.y)
