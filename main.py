import pygame
import sys
from Game import Game


def init_table():
    pygame.init()
    cell_size = 30
    cell_number = 20
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)
    game = Game(cell_number, cell_size, screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction('UP')
                if event.key == pygame.K_DOWN:
                    game.snake.change_direction('DOWN')
                if event.key == pygame.K_RIGHT:
                    game.snake.change_direction('RIGHT')
                if event.key == pygame.K_LEFT:
                    game.snake.change_direction('LEFT')
        game.draw()
        pygame.display.update()
        clock.tick(60)  # ruleaza cu max 60 frame-uri pe secunda


if __name__ == "__main__":
    init_table()
