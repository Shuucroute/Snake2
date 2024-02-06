import pygame
import sys
import time
import random
from pygame.locals import MOUSEBUTTONDOWN
from typing import List, Tuple

class Game:
    def __init__(self):
        pygame.init()
        self.FRAME_SIZE_X = 720
        self.FRAME_SIZE_Y = 480
        self.GAME_WINDOW = pygame.display.set_mode((self.FRAME_SIZE_X, self.FRAME_SIZE_Y))
        self.is_game_over = False
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        self.food_pos = [random.randrange(1, (self.FRAME_SIZE_X // 10)) * 10,
                         random.randrange(1, (self.FRAME_SIZE_Y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.DIFFICULTY = 15
        self.GAME_OVER_FLAG = False
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.FPS_CONTROLLER = pygame.time.Clock()
        self.RESTART_BUTTON_RECT = pygame.Rect(self.FRAME_SIZE_X / 4, self.FRAME_SIZE_Y / 1.5, 150, 50)
        self.QUIT_BUTTON_RECT = pygame.Rect(self.FRAME_SIZE_X / 2 + 20, self.FRAME_SIZE_Y / 1.5, 150, 50)

    def is_ended(self):
        return self.is_game_over

class EventManager:
    @staticmethod
    def handle_events(game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                EventManager.handle_keydown(event, game)
            elif event.type == MOUSEBUTTONDOWN:
                EventManager.handle_mouse_click(event, game)

    @staticmethod
    def handle_keydown(event, game):
        if event.key == pygame.K_UP or event.key == ord('z'):
            game.change_to = 'UP'
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            game.change_to = 'DOWN'
        if event.key == pygame.K_LEFT or event.key == ord('q'):
            game.change_to = 'LEFT'
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            game.change_to = 'RIGHT'
        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    @staticmethod
    def handle_mouse_click(event, game):
        if event.button == 1:
            if game.RESTART_BUTTON_RECT.collidepoint(event.pos):
                SnakeGameLogic.reset_game(game)
            elif game.QUIT_BUTTON_RECT.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

class DisplayManager:
    @staticmethod
    def render(game, surface):
        if game.GAME_OVER_FLAG:
            DisplayManager.display_game_over(game, surface)
        else:
            SnakeGameLogic.update(game, game.FPS_CONTROLLER)
            DisplayManager.display_game(game, surface)
        pygame.display.flip()

    @staticmethod
    def display_game(game, surface):
        surface.fill(game.BLACK)
        for pos in game.snake_body:
            pygame.draw.rect(surface, game.GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(surface, game.WHITE, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))
        SnakeGameDisplay.show_score(game, 1, game.WHITE, 'consolas', 20)

    @staticmethod
    def display_game_over(game, surface):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, game.RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (game.FRAME_SIZE_X / 2, game.FRAME_SIZE_Y / 4)
        surface.fill(game.BLACK)
        surface.blit(game_over_surface, game_over_rect)
        SnakeGameDisplay.show_score(game, 0, game.RED, 'times new roman', 20)
        game_over_text_surface = pygame.font.SysFont('times new roman', 30).render('Click to restart or QUIT', True, game.WHITE)
        game_over_text_rect = game_over_text_surface.get_rect()
        game_over_text_rect.midtop = (game.FRAME_SIZE_X / 2, game.FRAME_SIZE_Y / 1.5)
        surface.blit(game_over_text_surface, game_over_text_rect)

class SnakeGameLogic:
    @staticmethod
    def update(game, clock):
        # Logique du jeu
        EventManager.handle_events(game)

        if not game.GAME_OVER_FLAG:
            if game.change_to == 'UP' and game.direction != 'DOWN':
                game.direction = 'UP'
            if game.change_to == 'DOWN' and game.direction != 'UP':
                game.direction = 'DOWN'
            if game.change_to == 'LEFT' and game.direction != 'RIGHT':
                game.direction = 'LEFT'
            if game.change_to == 'RIGHT' and game.direction != 'LEFT':
                game.direction = 'RIGHT'

        if game.direction == 'UP':
            game.snake_pos[1] -= 10
        if game.direction == 'DOWN':
            game.snake_pos[1] += 10
        if game.direction == 'LEFT':
            game.snake_pos[0] -= 10
        if game.direction == 'RIGHT':
            game.snake_pos[0] += 10

        game.snake_body.insert(0, list(game.snake_pos))
        if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
            game.score += 1
            game.food_spawn = False
        else:
            game.snake_body.pop()

        if not game.food_spawn:
            game.food_pos = [random.randrange(1, (game.FRAME_SIZE_X // 10)) * 10,
                             random.randrange(1, (game.FRAME_SIZE_Y // 10)) * 10]
        game.food_spawn = True

        game.GAME_WINDOW.fill(game.BLACK)
        for pos in game.snake_body:
            pygame.draw.rect(game.GAME_WINDOW, game.GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game.GAME_WINDOW, game.WHITE, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

        if game.snake_pos[0] < 0 or game.snake_pos[0] > game.FRAME_SIZE_X-10:
            SnakeGameLogic.game_over(game)
        if game.snake_pos[1] < 0 or game.snake_pos[1] > game.FRAME_SIZE_Y-10:
            SnakeGameLogic.game_over(game)
        for block in game.snake_body[1:]:
            if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
                SnakeGameLogic.game_over(game)

        SnakeGameDisplay.show_score(game, 1, game.WHITE, 'consolas', 20)
        pygame.display.update()
        clock.tick(game.DIFFICULTY)

    @staticmethod
    def game_over(game):
        game.GAME_OVER_FLAG = True

    @staticmethod
    def reset_game(game):
        game.GAME_OVER_FLAG = False
        game.snake_pos = [100, 50]
        game.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        game.food_pos = [random.randrange(1, (game.FRAME_SIZE_X // 10)) * 10,
                         random.randrange(1, (game.FRAME_SIZE_Y // 10)) * 10]
        game.food_spawn = True
        game.direction = 'RIGHT'
        game.change_to = game.direction
        game.score = 0

class SnakeGameDisplay:
    @staticmethod
    def show_score(game, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(game.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (game.FRAME_SIZE_X / 10, 15)
        else:
            score_rect.midtop = (game.FRAME_SIZE_X / 2, game.FRAME_SIZE_Y / 1.25)
        game.GAME_WINDOW.blit(score_surface, score_rect)

def main():
    game = Game()

    while not game.is_ended():
        EventManager.handle_events(game)
        DisplayManager.render(game, game.GAME_WINDOW)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
