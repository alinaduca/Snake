import pygame
from pygame.math import Vector2
obstacle_color = (56, 74, 12)


class Obstacle:
    def __init__(self, coordinates):
        self.cactus = pygame.image.load('Images/cactus.png').convert_alpha()
        self.positions = []
        for coord in coordinates:
            self.positions.append(Vector2(coord['x'], coord['y']))

    def draw(self, size, surface):
        for pos in self.positions:
            obstacle_rectangle = pygame.Rect(int(pos.x * size), int(pos.y * size), size, size)
            if size == 30:
                surface.blit(self.cactus, obstacle_rectangle)
            else:
                pygame.draw.rect(surface, obstacle_color, obstacle_rectangle)
