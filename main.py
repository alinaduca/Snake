import pygame
import sys
import random

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
width = 800
height = 600
snake_block = 10
snake_speed = 10
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    font = pygame.font.SysFont(None, 50)
    screen_text = font.render(msg, True, color)
    game_display.blit(screen_text, [width / 6, height / 3])


def game_loop():
    game_over = False
    game_close = False
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1
    foodx = int(round(random.randrange(0, width - snake_block) / 10.0) * 10.0)
    foody = int(round(random.randrange(0, height - snake_block) / 10.0) * 10.0)
    print(foodx, foody)
    while not game_over:
        while game_close:
            game_display.fill(black)
            message("Ai pierdut! Apasă Q pentru a ieși sau C pentru a încerca din nou", red)
            our_snake(snake_block, snake_list)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        x1 += x1_change
        y1 += y1_change
        game_display.fill(black)
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])
        our_snake(snake_block, snake_list)
        # if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        #     game_close = True
        if x1 >= width:
            x1 = 0
        if x1 < 0:
            x1 = width - 1
        if y1 >= height:
            y1 = 0
        if y1 < 0:
            y1 = height - 1
        if x1 == foodx and y1 == foody:
            print("Egal")
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            print(foodx, foody)
            length_of_snake += 1
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)
    pygame.quit()
    sys.exit()


game_loop()
