from Fruit import Fruit
from Snake import Snake


class Game:
    def __init__(self, cell_number):
        self.fruit = Fruit(cell_number)
        self.snake = Snake()

    def update(self):
        self.snake.move()
        self.check_collision()

    def draw(self, cell_size, surface):
        self.fruit.draw(cell_size, surface)
        self.snake.draw(cell_size, surface)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

