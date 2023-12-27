import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self, size, surface):
        for block in self.body:
            block_rectangle = pygame.Rect(int(block.x * size), int(block.y * size), size, size)
            pygame.draw.rect(surface, (253, 70, 72), block_rectangle)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def change_direction(self, new_direction):
        match new_direction:
            case 'UP':
                self.direction = Vector2(0, -1)
            case 'DOWN':
                self.direction = Vector2(0, 1)
            case 'RIGHT':
                self.direction = Vector2(1, 0)
            case 'LEFT':
                self.direction = Vector2(-1, 0)

    def add_block(self):
        self.new_block = True

    # def check_fail(self):

