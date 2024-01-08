import pygame
from pygame.math import Vector2

# Definirea culorii abstacolelor
obstacle_color = (56, 74, 12)


class Obstacle:
    def __init__(self, coordinates):
        '''
        Inițializarea listei cu coordonatele eventualelor obstacole pe tabla de joc.
        :param coordinates: Coordonatele obstacolelor, sau o listă goală dacă nu există obstacole.
        '''
        self.cactus = pygame.image.load('Images/cactus.png').convert_alpha()
        self.positions = []
        for coord in coordinates:
            self.positions.append(Vector2(coord['x'], coord['y']))

    def draw(self, size, surface):
        '''
        Desenarea obstacolelor, un obstacol fiind reprezentat printr-un cactus (dacă size este egal cu 30) sau
        printr-un pătrat (în cazul unei alte valori pentru size)
        :param size: Mărimea unei celule de pe tabla de joc (presupunând și mărimea unui obstacol)
        :param surface: Display-ul pygame
        '''
        for pos in self.positions:
            obstacle_rectangle = pygame.Rect(int(pos.x * size), int(pos.y * size), size, size)
            if size == 30:
                surface.blit(self.cactus, obstacle_rectangle)
            else:
                pygame.draw.rect(surface, obstacle_color, obstacle_rectangle)
