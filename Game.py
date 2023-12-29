import pygame
from Fruit import Fruit
from Snake import Snake

light_green = (175, 215, 70)
text_color = (56, 74, 12)
light_text_color = (200, 200, 50)


class Game:
    def __init__(self, cell_number, cell_size, surface):
        self.current_score = 0
        self.record = 0
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.snake = Snake(cell_number)
        self.fruit = Fruit(cell_number, self.snake.body)
        self.size = cell_number
        self.cell_size = cell_size
        self.surface = surface
        self.game_over = False
        self.end = False

    def update(self):
        if not self.game_over and self.snake.get_is_moving():
            self.snake.move()
            self.check_collision()
            self.check_fail()

    def draw(self):
        if self.game_over:
            if not self.end:
                self.draw_game_over()
            else:
                self.draw_end_session()
        else:
            self.surface.fill(light_green)
            self.draw_grass()
            self.fruit.draw(self.cell_size, self.surface)
            self.snake.draw(self.cell_size, self.surface)
            self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.fruit.randomize(self.snake.body)
            self.snake.play_eating_sound()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over = True
                if self.record < self.current_score:
                    self.record = self.current_score

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(self.size):
            if row % 2 == 0:
                for col in range(self.size):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size,
                                                 self.cell_size)
                        pygame.draw.rect(self.surface, grass_color, grass_rect)
            else:
                for col in range(self.size):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size,
                                                 self.cell_size)
                        pygame.draw.rect(self.surface, grass_color, grass_rect)

    def draw_score(self):
        font = pygame.font.Font(None, 30)
        self.current_score = (len(self.snake.body) - 3) * 10
        score_text = ": " + str(self.current_score)
        score_surface = font.render(score_text, True, text_color)
        score_x = int(self.cell_size * self.size - 60)
        score_y = int(self.cell_size * self.size - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple = self.fruit.get_apple()
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 5, apple_rect.top - 4, apple_rect.width + score_rect.width + 10,
                              apple_rect.height + 8)

        pygame.draw.rect(self.surface, (167, 209, 61), bg_rect)
        self.surface.blit(score_surface, score_rect)
        self.surface.blit(apple, apple_rect)
        pygame.draw.rect(self.surface, text_color, bg_rect, 2)

    def draw_game_over(self):
        font = pygame.font.Font(None, 35)
        current_score_text = "Score: " + str(self.current_score)
        current_score_surface = font.render(current_score_text, True, text_color)
        current_score_x = int(self.cell_size * self.size / 2)
        current_score_y = int(self.cell_size * self.size / 7 * 3)
        current_score_rect = current_score_surface.get_rect(midbottom=(current_score_x, current_score_y))

        end_session_text = "End session?"
        yes_text = "y - Yes"
        no_text = "n - No"
        font2 = pygame.font.Font(None, 28)
        end_session_surface = font2.render(end_session_text, True, text_color)
        yes_surface = font2.render(yes_text, True, text_color)
        no_surface = font2.render(no_text, True, text_color)
        end_session_x = int(self.cell_size * self.size / 2)
        end_session_y = int(self.cell_size * self.size / 7 * 4)
        end_session_rect = end_session_surface.get_rect(midtop=(end_session_x, end_session_y))
        yes_rect = yes_surface.get_rect(midtop=(end_session_x, end_session_rect.bottom))
        no_rect = no_surface.get_rect(midtop=(end_session_x, yes_rect.bottom))

        frame_rect = pygame.Rect(end_session_rect.left - 10, current_score_rect.top - 8,
                                 max(end_session_rect.width, current_score_rect.width) + 20,
                                 (end_session_rect.top - current_score_rect.top) + end_session_rect.height +
                                 yes_rect.height + no_rect.height + 16)

        self.surface.blit(current_score_surface, current_score_rect)
        self.surface.blit(end_session_surface, end_session_rect)
        self.surface.blit(yes_surface, yes_rect)
        self.surface.blit(no_surface, no_rect)
        pygame.draw.rect(self.surface, text_color, frame_rect, 2)

    def continue_session(self):
        if self.game_over:
            self.game_over = False
            self.current_score = 0
            self.snake.reset()

    def end_session(self):
        if self.game_over:
            self.end = True

    def draw_end_session(self):
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 42)
        record_x = int(self.cell_size * self.size / 2)
        record_y = int(self.cell_size * self.size / 2)
        record_text = "High Score: " + str(self.record)
        record_surface = font.render(record_text, True, light_text_color)
        record_rect = record_surface.get_rect(center=(record_x, record_y))
        self.surface.blit(record_surface, record_rect)
