import pygame
from pygame.math import Vector2
obstacle_color = (56, 74, 12)


class Obstacle:
    def __init__(self):
        self.pos = Vector2(5, 10)

    def draw(self, size, surface):
        obstacle_rectangle = pygame.Rect(int(self.pos.x * size), int(self.pos.y * size), size, size)
        pygame.draw.rect(surface, obstacle_color, obstacle_rectangle)
