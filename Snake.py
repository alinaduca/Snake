import pygame
from pygame.math import Vector2
snake_color = (106, 158, 104)


class Snake:
    def __init__(self, cells):
        '''
        Inițializarea șarpelui: pozițoa inițială pe tabla de joc, flag-uri, direcția, sunetul pentru mușcătură și
        imaginile pentru toate segmentele posibile din corp.
        :param cells: Numărul de celule
        '''
        self.body = [Vector2(14, 10), Vector2(15, 10), Vector2(16, 10)]
        self.direction = Vector2(0, 0)
        self.cells = cells
        self.new_block = False
        self.is_moving = False

        self.head = None
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()

        self.tail = None
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()
        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()

        self.eating_sound = pygame.mixer.Sound('Sounds/eating.mp3')

    def draw(self, size, surface):
        '''
        Desenarea șarpelui pe tabla de joc.
        :param size: Dimensiunea unui block
        :param surface: Display-ul pygame
        '''
        if size != 30:
            for block in self.body:
                x_pos = int(block.x * size)
                y_pos = int(block.y * size)
                block_rectangle = pygame.Rect(x_pos, y_pos, size, size)
                pygame.draw.rect(surface, snake_color, block_rectangle)
        else:
            self.update_head_graphics()
            self.update_tail_graphics()
            for index, block in enumerate(self.body):
                x_pos = int(block.x * size)
                y_pos = int(block.y * size)
                block_rectangle = pygame.Rect(x_pos, y_pos, size, size)
                if index == 0:
                    surface.blit(self.head, block_rectangle)
                elif index == len(self.body) - 1:
                    surface.blit(self.tail, block_rectangle)
                else:
                    previous_block = self.body[index + 1] - block
                    next_block = self.body[index - 1] - block
                    if previous_block.x == next_block.x:
                        surface.blit(self.body_vertical, block_rectangle)
                    elif previous_block.y == next_block.y:
                        surface.blit(self.body_horizontal, block_rectangle)
                    else:
                        if abs(previous_block.x) >= self.cells - 1:
                            previous_block.x = (-1) ** (previous_block.x > 0)
                        elif abs(previous_block.y) >= self.cells - 1:
                            previous_block.y = (-1) ** (previous_block.y > 0)
                        elif abs(next_block.x) >= self.cells - 1:
                            next_block.x = (-1) ** (next_block.x > 0)
                        elif abs(next_block.y) >= self.cells - 1:
                            next_block.y = (-1) ** (next_block.y > 0)

                        if (previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and
                                next_block.x == -1):
                            surface.blit(self.body_bl, block_rectangle)
                        elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                            surface.blit(self.body_tr, block_rectangle)
                        elif (previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and
                              next_block.x == -1):
                            surface.blit(self.body_tl, block_rectangle)
                        elif (previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and
                              next_block.x == 1):
                            surface.blit(self.body_br, block_rectangle)

    def move(self):
        '''
        Logica pentru înaintarea/mutarea șarpelui pe tabla de joc.
        '''
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        if not 0 <= body_copy[0].y:
            body_copy[0].y = self.cells - 1
        if not body_copy[0].x < self.cells:
            body_copy[0].x = 0
        if not body_copy[0].y < self.cells:
            body_copy[0].y = 0
        if not 0 <= body_copy[0].x:
            body_copy[0].x = self.cells - 1
        self.body = body_copy[:]

    def change_direction(self, new_direction):
        '''
        Schimbarea direcției șarpelui pe tabla de joc.
        :param new_direction: Noua direcție de mișcare a șarpelui.
        '''
        self.is_moving = True
        old_direction = self.direction
        match new_direction:
            case 'UP':
                if old_direction != Vector2(0, 1):
                    self.direction = Vector2(0, -1)
            case 'DOWN':
                if old_direction != Vector2(0, -1):
                    self.direction = Vector2(0, 1)
            case 'RIGHT':
                if old_direction != Vector2(-1, 0):
                    self.direction = Vector2(1, 0)
            case 'LEFT':
                if old_direction != Vector2(1, 0):
                    self.direction = Vector2(-1, 0)

    def add_block(self):
        '''
        Adăugarea unui block nou la corpul șarpelui.
        :return:
        '''
        self.new_block = True

    def update_head_graphics(self):
        '''
        Schimbarea imaginii pentru capul șarpelui, în funcție de noua direcție.
        '''
        current_direction = self.body[0] - self.body[1]
        if current_direction == Vector2(0, 1):
            self.head = self.head_down
        elif current_direction == Vector2(0, -1):
            self.head = self.head_up
        elif current_direction == Vector2(1, 0):
            self.head = self.head_right
        elif current_direction == Vector2(-1, 0):
            self.head = self.head_left

    def update_tail_graphics(self):
        '''
        Schimbarea imaginii pentru coada șarpelui, în funcție de noua direcție.
        '''
        current_direction = self.body[-2] - self.body[-1]
        if current_direction == Vector2(0, 1):
            self.tail = self.tail_down
        elif current_direction == Vector2(0, -1):
            self.tail = self.tail_up
        elif current_direction == Vector2(1, 0):
            self.tail = self.tail_right
        elif current_direction == Vector2(-1, 0):
            self.tail = self.tail_left

    def reset(self):
        '''
        Resetarea șarpelui: dimensiunea inițială, poziția și direcția. Resetarea flag-urilor.
        :return:
        '''
        self.body = [Vector2(14, 10), Vector2(15, 10), Vector2(16, 10)]
        self.direction = Vector2(0, 0)
        self.is_moving = False
        self.new_block = False

    def get_is_moving(self):
        '''
        Getter pentru flagul is_moving
        :return: valoarea flagului is_moving (True sau False)
        '''
        return self.is_moving
