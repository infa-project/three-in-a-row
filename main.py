import pygame
import random
from board import *
from game_object import *
from button import *

WIDTH = 500
HEIGHT = 600
TOP_HOLLOW = 100
FPS = 30

SIZE = 10

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# подсчёт очков
score = 0

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

pygame.display.flip()

# Шрифт
FONT = pygame.font.SysFont('comicsansms', 40)
FONT1 = pygame.font.SysFont('comicsansms', 60)

GAME_OVER_TEXT_POSITION = (WIDTH // 6, HEIGHT // 3)
YOUR_SCORE_TEXT_POSITION = (WIDTH // 4, HEIGHT // 3 + 70)

running = True
initial_screen = True
game = False
game_over = False

while running and (initial_screen or game or game_over):
    # начало игры
    if running and initial_screen:
        # кнопка
        NEW_GAME_BUTTON = Button('NEW GAME', 11 * WIDTH // 40, HEIGHT // 2, 230, 60)
        NEW_GAME_BUTTON.create_button(screen, FONT, BLACK)

        # навзание игры
        screen.blit(FONT1.render('MATCH-THREE', 1, BLACK), (WIDTH // 15, HEIGHT // 4))

        pygame.display.flip()
        while running and initial_screen:
            # Держим цикл на правильной скорости
            clock.tick(FPS)
            for event in pygame.event.get():
                # проверяем, не закрыл ли пользователь окно
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEW_GAME_BUTTON.x <= event.pos[0] <= NEW_GAME_BUTTON.x + NEW_GAME_BUTTON.w \
                            and NEW_GAME_BUTTON.y <= event.pos[1] <= NEW_GAME_BUTTON.y + NEW_GAME_BUTTON.h:
                        initial_screen = False
                        game = True
                        screen.fill(WHITE)

    if game and running:
        # инициализируем доску
        board = Board(SIZE, WIDTH, HEIGHT, TOP_HOLLOW)
        board.draw_init(screen)
        board.draw(screen)

        # отображение количества очков
        score_text = FONT.render('Score: ' + str(score), 1, BLACK)
        SCORE_TEXT_POSITION = (10, 20)
        screen.blit(score_text, SCORE_TEXT_POSITION)

        # количество ходов
        moves = 20
        moves_text = FONT.render('Moves: ' + str(moves), 1, BLACK)
        MOVES_TEXT_POSITION = (WIDTH - 200, 20)
        screen.blit(moves_text, MOVES_TEXT_POSITION)

        # Цикл игры
        selected = False
        x_selected, y_selected = None, None
        while moves > 0 and running:
            # Держим цикл на правильной скорости
            clock.tick(FPS)
            # Ввод события
            for event in pygame.event.get():
                # проверяем, не закрыл ли пользователь окно
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not selected:
                        selected = True
                        (x_selected, y_selected) = board.get_coords(event.pos[0], event.pos[1])
                        if x_selected >= 0 and y_selected >= 0:
                            board.draw_selected(screen, x_selected, y_selected)
                        else:
                            selected = False
                            (x_selected, y_selected) = None, None
                    else:
                        board.erase_selected(screen, x_selected, y_selected)
                        (x2, y2) = board.get_coords(event.pos[0], event.pos[1])
                        dist = abs(x_selected - x2) + abs(y_selected - y2)
                        if x2 >= 0 and y2 >= 0:
                            if dist == 0:
                                selected = False
                            elif dist == 1:
                                if board.goal(round(x_selected), round(y_selected), round(x2), round(y2)):
                                    moves -= 1
                                    pygame.draw.rect(screen, WHITE, (250, 0, 250, 70))
                                    moves_text = FONT.render('Moves: ' + str(moves), 1, BLACK)
                                    screen.blit(moves_text, MOVES_TEXT_POSITION)

                                    board.swap(screen, round(x_selected), round(y_selected), round(x2), round(y2))
                                    score += board.boom(screen)
                                    board.fall(screen)
                                    board.draw(screen)
                                    while board.is_there_three_in_a_row():
                                        score += board.boom(screen)
                                        board.fall(screen)
                                        board.draw(screen)
                                    board.fill()

                                    # меняем очки на экране
                                    pygame.draw.rect(screen, WHITE, (0, 0, 250, 70))
                                    score_text = FONT.render('Score: ' + str(score), 1, BLACK)
                                    screen.blit(score_text, SCORE_TEXT_POSITION)

                                    selected = False
                                else:
                                    x_selected = x2
                                    y_selected = y2
                                    board.draw_selected(screen, x_selected, y_selected)
                            else:
                                x_selected = x2
                                y_selected = y2
                                board.draw_selected(screen, x_selected, y_selected)
                    board.draw(screen)

            if running:
                # После отрисовки всего обновляем экран
                pygame.display.flip()

        if moves <= 0 and running:
            game = False
            game_over = True

    if running and game_over:
        screen.fill(WHITE)

        game_over_text = FONT1.render('GAME OVER', 1, BLACK)
        screen.blit(game_over_text, GAME_OVER_TEXT_POSITION)

        your_score_text = FONT.render('Your score: ' + str(score), 1, BLACK)
        screen.blit(your_score_text, YOUR_SCORE_TEXT_POSITION)

        score = 0

        # рисуем стрелочку
        pygame.draw.aaline(screen, BLACK, (20, 50), (50, 50))
        pygame.draw.aaline(screen, BLACK, (20, 50), (30, 40))
        pygame.draw.aaline(screen, BLACK, (20, 50), (30, 60))

        pygame.display.flip()

        while running and game_over:
            clock.tick(FPS)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 <= event.pos[0] <= 60 and 0 <= event.pos[1] <= 60:
                        initial_screen = True
                        game_over = False
                        screen.fill(WHITE)
                        pygame.display.flip()

pygame.quit()