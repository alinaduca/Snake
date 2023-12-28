import pygame
import sys
from Fruit import Fruit
from Snake import Snake


class Game:
    def __init__(self, cell_number, cell_size):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.snake = Snake(cell_number)
        self.fruit = Fruit(cell_number, self.snake.body)
        self.size = cell_number
        self.cell_size = cell_size

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()
        # self.check_out_of_screen()

    def draw(self, surface):
        self.draw_grass(surface)
        self.fruit.draw(self.cell_size, surface)
        self.snake.draw(self.cell_size, surface)
        self.draw_score(surface)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.fruit.randomize(self.snake.body)
            self.snake.play_eating_sound()

    def game_over(self):
        # pygame.quit()
        # sys.exit()
        self.snake.reset()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self, surface):
        grass_color = (167, 209, 61)
        for row in range(self.size):
            if row % 2 == 0:
                for col in range(self.size):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(surface, grass_color, grass_rect)
            else:
                for col in range(self.size):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(surface, grass_color, grass_rect)

    def draw_score(self, surface):
        font = pygame.font.Font(None, 30)
        score_text = ": " + str((len(self.snake.body) - 3) * 10)
        score_surface = font.render(score_text, True, (56, 74, 12))
        score_x = int(self.cell_size * self.size - 60)
        score_y = int(self.cell_size * self.size - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple = self.fruit.get_apple()
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 5, apple_rect.top - 4, apple_rect.width + score_rect.width + 10, apple_rect.height + 8)

        pygame.draw.rect(surface, (167, 209, 61), bg_rect)
        surface.blit(score_surface, score_rect)
        surface.blit(apple, apple_rect)
        pygame.draw.rect(surface, (56, 74, 12), bg_rect, 2)


    # def check_out_of_screen(self):
    #     if not 0 <= self.snake.body[0].x <= self.size or not 0 <= self.snake.body[0].y <= self.size:
    #         # print('Finished because  self.snake.body[0].x = ', str(self.snake.body[0].x), ' self.snake.body[0].y=',  str(self.snake.body[0].y), 'and self.size=', str(self.size))
    #         self.game_over()
