import pygame
import random
from pygame.math import Vector2

# Definirea culorii fructului
fruit_color = (217, 1, 2)


class Fruit:
    def __init__(self, cells, snake_body, obstacles_pos):
        '''
        Inițializarea fructului: imaginea și poziția lui.
        :param cells: Numărul de celule pe tabla de joc.
        :param snake_body: Coordonatele corpului șarpelui.
        :param obstacles_pos: Coordonatele obstacolelor pe hartă.
        '''
        self.x = 0
        self.y = 0
        self.pos = Vector2(self.x, self.y)
        self.max_pos = cells - 1
        self.randomize(snake_body, obstacles_pos)
        self.apple = pygame.image.load('Images/apple.png').convert_alpha()

    def draw(self, size, surface):
        '''
        Desenarea fructului pe tabla de joc, un fruct fiind reprezentat printr-un măr (dacă size este egal cu 30) sau
        printr-un pătrat de culoare roșie (în cazul unei alte valori pentru size)
        :param size: Mărimea unei celule de pe tabla de joc (presupunând și mărimea fructului)
        :param surface: Display-ul pygame
        '''
        fruit_rectangle = pygame.Rect(int(self.pos.x * size), int(self.pos.y * size), size, size)
        if size == 30:
            surface.blit(self.apple, fruit_rectangle)
        else:
            pygame.draw.rect(surface, fruit_color, fruit_rectangle)

    def randomize(self, snake_body, obstacles_pos):
        '''
        Noua poziție a fructului, calculată random. Se va avea grijă ca poziția fructului să nu se intersecteze cu
        poziția corpului șarpelui, a vreunui obstacol sau a scorului.
        :param snake_body: Coordonatele blocurilor din corpul șarpelui
        :param obstacles_pos: Coordonatele obstacolelor
        '''
        while True:
            self.x = random.randint(0, self.max_pos)
            self.y = random.randint(0, self.max_pos)
            self.pos = Vector2(self.x, self.y)
            if (self.pos not in snake_body and self.pos not in obstacles_pos and
                    self.x < self.max_pos - 3 and self.y < self.max_pos - 1):
                break

    def get_apple(self):
        '''
        Getter pentru imaginea mărului.
        :return: valoarea memorată în self.apple reprezentând imaginea mărului.
        '''
        return self.apple
