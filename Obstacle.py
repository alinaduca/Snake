import pygame
from pygame.math import Vector2


class Obstacle:
    def __init__(self, coordinates):
        self.cactus = pygame.image.load('Images/cactus.png').convert_alpha()
        self.positions = []
        for coord in coordinates:
            self.positions.append(Vector2(coord['x'], coord['y']))

    def draw(self, size, surface):
        for pos in self.positions:
            obstacle_rectangle = pygame.Rect(int(pos.x * size), int(pos.y * size), size, size)
            surface.blit(self.cactus, obstacle_rectangle)
