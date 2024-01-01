import pygame
import json
import sys
from Game import Game


def read_json(json_file):
    """
    Citirea conținutului fișierului json.
    :param json_file: Numele unui fișier json
    :return: un dicționar cu conținutul fișierului json sau None, dacă
    este inexistent, extensie incorectă sau fișier gol.
    """
    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            if not json_data:
                raise ValueError("The JSON file is empty.")
            return json_data
    except FileNotFoundError:
        print('Error: File ' + json_file + ' not found.')
        return None
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON in file " + json_file + ".")
        return None
    except ValueError as e:
        print("Error: " + str(e))
        return None


def init_table(dictionary):
    """
    Inițializarea tablei de joc.
    :param dictionary: Informații privind dimensiunea tablei și a coordonatelor obstacolelor.
    """
    pygame.init()
    if 'cells' not in dictionary:
        dictionary['cells'] = 20
    if 'size_of_a_cell' not in dictionary:
        dictionary['size_of_a_cell'] = 30
    screen = pygame.display.set_mode((dictionary['cells'] * dictionary['size_of_a_cell'],
                                      dictionary['cells'] * dictionary['size_of_a_cell']))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)
    game = Game(dictionary['cells'], dictionary['size_of_a_cell'], screen)
    if 'obstacles' in dictionary:
        game.set_obstacles(dictionary['obstacles'])
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
                if event.key == pygame.K_n:
                    game.continue_session()
                if event.key == pygame.K_y:
                    game.end_session()
                if event.key == pygame.K_s:
                    game.start_session()
                if event.key == pygame.K_q:
                    game.quit()
        game.draw()
        pygame.display.update()
        clock.tick(60)  # ruleaza cu max 60 frame-uri pe secunda


if __name__ == "__main__":
    '''
        Aici verific dacă s-a lansat comanda cu numărul corect de argumente,
        în caz afirmativ urmând să citesc informațiile din fișierul json dat în linia de comandă
        și să inițializez tabla de joc.
    '''
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <json_file>")
    else:
        data = read_json(sys.argv[1])
        if data is not None:
            init_table(data)
