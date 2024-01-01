import pygame
import sys
from Fruit import Fruit
from Snake import Snake
from Obstacle import Obstacle

# Definirea culorilor care vor fi folosite
light_green = (175, 215, 70)
grass_color = (167, 209, 61)
dark_text_color = (56, 74, 12)
light_text_color = (200, 200, 50)


class Game:
    """
        Clasă în care voi avea toată logica jocului, componentele și funcțiile importante.
    """
    def __init__(self, cells, size_of_a_cell, surface):
        """
        Inițializarea jocului: dimensiunile tablei, suprafața și flag-uri.
        :param cells: Numărul de celule ale tablei e joc. Numărul default este 20.
        :param size_of_a_cell: Dimensiunea unei astfel de celule. Dimensiunea default este 30.
        :param surface: Display-ul pygame.
        """
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.current_score = 0
        self.record = 0
        self.snake = Snake(cells)
        self.obstacles = Obstacle([])
        self.fruit = Fruit(cells, self.snake.body, [])
        self.size = cells
        self.size_of_a_cell = size_of_a_cell
        self.surface = surface
        self.game_over = False
        self.end = False

    def update(self):
        """
        Updatarea interacțiunilor din joc și verificarea coliziunilor.
        """
        if not self.game_over and self.snake.get_is_moving():
            self.snake.move()
            self.check_collision_with_apple()
            self.check_collision_with_obstacle()
            self.check_fail()

    def set_obstacles(self, coordinates):
        """
        Dacă în json-ul dat la consolă conține coordonate ale obstacolelor, aici vor fi setate.
        :param coordinates: Coordonatele obstacolelor pe hartă / tabla de joc.
        """
        self.obstacles = Obstacle(coordinates)
        if self.fruit.pos in self.obstacles.positions:
            self.fruit.randomize(self.snake.body, self.obstacles.positions)

    def draw(self):
        """
        Desenarea cpmponentelor pe tabla de joc. Dacă jocul a fost pierdut, atunci se apelează self.draw_game_over().
        Dacă sesiunea a fost încheiată, se va apela self.draw_end_session().
        Altfel, toate componentele (fructul, șarpele, scorul, iarba, eventualele obstacole) vor fi afișate.
        """
        if self.game_over:
            if not self.end:
                self.draw_game_over()
            else:
                self.draw_end_session()
        else:
            self.surface.fill(light_green)
            self.draw_darker_squares()
            self.obstacles.draw(self.size_of_a_cell, self.surface)
            self.fruit.draw(self.size_of_a_cell, self.surface)
            self.snake.draw(self.size_of_a_cell, self.surface)
            self.draw_score()

    def check_collision_with_apple(self):
        """
        Verific dacă șarpele s-a ciocnit cu fructul, adică dacă coordonatele capului coincid cu coordonatele fructului.
        În caz afirmativ, adaug un bloc nou în corpul șarpelui, calculez alte coordonate pentru fruct și încep sunetul
        pentru mușcătură.
        """
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.fruit.randomize(self.snake.body, self.obstacles.positions)
            self.snake.eating_sound.play()

    def check_collision_with_obstacle(self):
        """
        Verific dacă șarpele s-a ciocnit cu un obstacol, adică dacă coordonatele capului coincid cu coordonatele
        vreunui obstacol iterând prin lista self.obstacles.positions.
        """
        if self.obstacles is not None:
            for pos in self.obstacles.positions:
                if pos == self.snake.body[0]:
                    self.game_over = True
                    if self.record < self.current_score:
                        self.record = self.current_score

    def check_fail(self):
        """
        Verific dacă șarpele s-a ciocnit cu vreo porțiune din propriul său corp, începând cu al treilea bloc (pentru că,
        în reprezentarea vizuală, nu există niciun caz în care primul bloc s-ar putea izbi de al doilea, în afară de
        cazul în care șarpele efectuează o rotație de 180°, caz care nu se permite (nefiind luat în considerare
        încă din main.py). Dacă ciocnirea are loc, se setează flag-ul game_over și (eventual) se actualizează recordul.
        """
        for block in self.snake.body[2:]:
            if block == self.snake.body[0]:
                self.game_over = True
                if self.record < self.current_score:
                    self.record = self.current_score

    def draw_darker_squares(self):
        """
        Desenarea unor pătrate mai închise (reprezentând iarba) pe tabla de joc pentru urmărirea mai facilă a fructelor
        sau a obstacolelor.
        """
        for row in range(self.size):
            if row % 2 == 0:
                for column in range(self.size):
                    if column % 2 == 0:
                        grass_rectangle = pygame.Rect(column * self.size_of_a_cell, row * self.size_of_a_cell,
                                                      self.size_of_a_cell, self.size_of_a_cell)
                        pygame.draw.rect(self.surface, grass_color, grass_rectangle)
            else:
                for column in range(self.size):
                    if column % 2 != 0:
                        grass_rectangle = pygame.Rect(column * self.size_of_a_cell, row * self.size_of_a_cell,
                                                      self.size_of_a_cell, self.size_of_a_cell)
                        pygame.draw.rect(self.surface, grass_color, grass_rectangle)

    def draw_score(self):
        """
        Afișarea scorului în colțul din dreapta-jos al ecranului.
        """
        font = pygame.font.Font(None, 30)
        self.current_score = (len(self.snake.body) - 3) * 10
        score_text = ": " + str(self.current_score)
        score_surface = font.render(score_text, True, dark_text_color)
        score_x = int(self.size_of_a_cell * self.size - 60)
        score_y = int(self.size_of_a_cell * self.size - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple = self.fruit.get_apple()
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 5, apple_rect.top - 4, apple_rect.width + score_rect.width + 10,
                              apple_rect.height + 8)

        pygame.draw.rect(self.surface, (167, 209, 61), bg_rect)
        self.surface.blit(score_surface, score_rect)
        self.surface.blit(apple, apple_rect)
        pygame.draw.rect(self.surface, dark_text_color, bg_rect, 2)

    def draw_game_over(self):
        """
        Afișarea meniului la momentul în care utilizatorul a pierdut jocul.
        """
        font = pygame.font.Font(None, 35)
        current_score_text = "Score: " + str(self.current_score)
        current_score_surface = font.render(current_score_text, True, dark_text_color)
        current_score_x = int(self.size_of_a_cell * self.size / 2)
        current_score_y = int(self.size_of_a_cell * self.size / 7 * 3)
        current_score_rect = current_score_surface.get_rect(midbottom=(current_score_x, current_score_y))

        end_session_text = "End session?"
        yes_text = "y - Yes"
        no_text = "n - No"
        font2 = pygame.font.Font(None, 28)
        end_session_surface = font2.render(end_session_text, True, dark_text_color)
        yes_surface = font2.render(yes_text, True, dark_text_color)
        no_surface = font2.render(no_text, True, dark_text_color)
        end_session_x = int(self.size_of_a_cell * self.size / 2)
        end_session_y = int(self.size_of_a_cell * self.size / 7 * 4)
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
        pygame.draw.rect(self.surface, dark_text_color, frame_rect, 2)

    def continue_session(self):
        """
        Resetez tabla de joc, poziția și dimensiunile șarpelui pe tablă și încep o nouă sesiune de joc.
        """
        if self.game_over:
            self.game_over = False
            self.current_score = 0
            self.snake.reset()

    def end_session(self):
        """
        Dacă utilizatorul alege să încheie sesiunea, iar flag-ul game_over este true (pentru a ști că utilizatorul a
        apăsat tasta corespunzătoare în momentul potrivit, ci nu în mijlocul jocului), atunci setez flag-ul self.end pe
        true pentru a anunța că sesiunea de joc este încheiată.
        """
        if self.game_over:
            self.end = True

    def draw_end_session(self):
        """
        Afișarea ecranului la terminarea unei sesiuni de joc, conținând recordul și noul meniu.
        """
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 42)
        record_x = int(self.size_of_a_cell * self.size / 2)
        record_y = int(self.size_of_a_cell * self.size / 2)
        record_text = "High Score: " + str(self.record)
        record_surface = font.render(record_text, True, light_text_color)
        record_rect = record_surface.get_rect(center=(record_x, record_y))
        self.surface.blit(record_surface, record_rect)

        session_text = "Starting new session?"
        start_text = "s - Start new session"
        quit_text = "q - Quit"
        font1 = pygame.font.Font(None, 28)
        start_session_surface = font1.render(session_text, True, light_text_color)
        yes_surface = font1.render(start_text, True, light_text_color)
        quit_surface = font1.render(quit_text, True, light_text_color)
        end_session_x = int(self.size_of_a_cell * self.size / 2)
        end_session_y = int(self.size_of_a_cell * self.size / 7 * 4)
        start_session_rect = start_session_surface.get_rect(midtop=(end_session_x, end_session_y))
        yes_rect = yes_surface.get_rect(midtop=(end_session_x, start_session_rect.bottom))
        quit_rect = quit_surface.get_rect(midtop=(end_session_x, yes_rect.bottom))

        self.surface.blit(start_session_surface, start_session_rect)
        self.surface.blit(yes_surface, yes_rect)
        self.surface.blit(quit_surface, quit_rect)

    def start_session(self):
        """
        Începerea unei sesiuni noi din interfața existentă.
        """
        if self.end:
            self.end = False
            self.game_over = False
            self.current_score = 0
            self.record = 0
            self.snake.reset()

    def quit(self):
        """
        Închiderea ecranului, terminarea execuției programului.
        """
        if self.end:
            pygame.quit()
            sys.exit()
