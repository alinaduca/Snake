import pygame
from pygame.math import Vector2


class Obstacle:
    def __init__(self):
        self.pos = Vector2(5, 10)
        self.obstacle = pygame.image.load('Images/cactus.png').convert_alpha()

    def draw(self, size, surface):
        obstacle_rectangle = pygame.Rect(int(self.pos.x * size), int(self.pos.y * size), size, size)
        surface.blit(self.obstacle, obstacle_rectangle)
