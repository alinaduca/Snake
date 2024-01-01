import pygame
import random
from pygame.math import Vector2
fruit_color = (217, 1, 2)


class Fruit:
    def __init__(self, cells, snake_body, obstacles_pos):
        self.x = 0
        self.y = 0
        self.pos = Vector2(self.x, self.y)
        self.max_pos = cells - 1
        self.randomize(snake_body, obstacles_pos)
        self.apple = pygame.image.load('Images/apple.png').convert_alpha()

    def draw(self, size, surface):
        fruit_rectangle = pygame.Rect(int(self.pos.x * size), int(self.pos.y * size), size, size)
        if size == 30:
            surface.blit(self.apple, fruit_rectangle)
        else:
            pygame.draw.rect(surface, fruit_color, fruit_rectangle)

    def randomize(self, snake_body, obstacles_pos):
        while True:
            self.x = random.randint(0, self.max_pos)
            self.y = random.randint(0, self.max_pos)
            self.pos = Vector2(self.x, self.y)
            if (self.pos not in snake_body and self.pos not in obstacles_pos and
                    self.x < self.max_pos - 2 and self.y < self.max_pos - 1):
                break

    def get_apple(self):
        return self.apple
