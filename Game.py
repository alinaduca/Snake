import pygame
import sys
from Fruit import Fruit
from Snake import Snake


class Game:
    def __init__(self, cell_number):
        self.fruit = Fruit(cell_number)
        self.snake = Snake()
        self.size = cell_number

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_out_of_screen()
        # self.check_fail()

    def draw(self, cell_size, surface):
        self.fruit.draw(cell_size, surface)
        self.snake.draw(cell_size, surface)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                # self.game_over()
                print(block)

    def check_out_of_screen(self):
        if not 0 <= self.snake.body[0].x <= self.size or not 0 <= self.snake.body[0].y <= self.size:
            self.game_over()
