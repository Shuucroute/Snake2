"""
Snake Eater
Made with PyGame
"""

import pygame
import sys
import time
import random
from pygame.locals import MOUSEBUTTONDOWN
from typing import List, Tuple


class Game:
    def __init__(self):
        # Difficulty settings
        self.DIFFICULTY: int = 20
        self.FRAME_SIZE_X: int = 720
        self.FRAME_SIZE_Y: int = 480

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.GAME_WINDOW = pygame.display.set_mode((self.FRAME_SIZE_X, self.FRAME_SIZE_Y))

        # Colors (R, G, B)
        self.BLACK: pygame.Color = pygame.Color(0, 0, 0)
        self.WHITE: pygame.Color = pygame.Color(255, 255, 255)
        self.RED: pygame.Color = pygame.Color(255, 0, 0)
        self.GREEN: pygame.Color = pygame.Color(0, 255, 0)
        self.BLUE: pygame.Color = pygame.Color(0, 0, 255)

        # FPS (frames per second) controller
        self.FPS_CONTROLLER: pygame.time.Clock = pygame.time.Clock()

        # Game variables
        self.snake_pos: List[int] = [100, 50]
        self.snake_body: List[List[int]] = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos: List[int] = [random.randrange(1, (self.FRAME_SIZE_X // 10)) * 10,
                                    random.randrange(1, (self.FRAME_SIZE_Y // 10)) * 10]
        self.food_spawn: bool = True
        self.direction: str = 'RIGHT'
        self.change_to: str = self.direction
        self.score: int = 0
        self.GAME_OVER_FLAG: bool = False
        self.RESTART_BUTTON_RECT: pygame.Rect = pygame.Rect(self.FRAME_SIZE_X / 4, self.FRAME_SIZE_Y / 2, 200, 50)
        self.QUIT_BUTTON_RECT: pygame.Rect = pygame.Rect(self.FRAME_SIZE_X / 4, self.FRAME_SIZE_Y / 1.5, 200, 50)

    def is_ended(self) -> bool:
        return self.GAME_OVER_FLAG

    def update(self, clock: pygame.time.Clock) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('z'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('q'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.RESTART_BUTTON_RECT.collidepoint(event.pos):
                        self.GAME_OVER_FLAG = False
                        self.snake_pos = [100, 50]
                        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
                        self.food_pos = [random.randrange(1, (self.FRAME_SIZE_X // 10)) * 10,
                                         random.randrange(1, (self.FRAME_SIZE_Y // 10)) * 10]
                        self.food_spawn = True
                        self.direction = 'RIGHT'
                        self.change_to = self.direction
                        self.score = 0
                    elif self.QUIT_BUTTON_RECT.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        if not self.GAME_OVER_FLAG:
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.FRAME_SIZE_X // 10)) * 10,
                             random.randrange(1, (self.FRAME_SIZE_Y // 10)) * 10]
        self.food_spawn = True

        self.GAME_WINDOW.fill(self.BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.GAME_WINDOW, self.GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(self.GAME_WINDOW, self.WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.FRAME_SIZE_X-10:
            self.game_over()
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.FRAME_SIZE_Y-10:
            self.game_over()
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over()

        self.show_score(1, self.WHITE, 'consolas', 20)
        pygame.display.update()
        clock.tick(self.DIFFICULTY)

    def render(self, surface: pygame.Surface) -> None:
        if self.GAME_OVER_FLAG:
            my_font = pygame.font.SysFont('times new roman', 90)
            game_over_surface = my_font.render('YOU DIED', True, self.RED)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (self.FRAME_SIZE_X / 2, self.FRAME_SIZE_Y / 4)
            surface.fill(self.BLACK)
            surface.blit(game_over_surface, game_over_rect)
            self.show_score(0, self.RED, 'times', 20)
            pygame.display.flip()
            time.sleep(3)
            pygame.quit()
            sys.exit()

    def show_score(self, choice: int, color: pygame.Color, font: str, size: int) -> None:
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.FRAME_SIZE_X / 10, 15)
        else:
            score_rect.midtop = (self.FRAME_SIZE_X / 2, self.FRAME_SIZE_Y / 1.25)
        self.GAME_WINDOW.blit(score_surface, score_rect)

    def game_over(self) -> None:
        self.GAME_OVER_FLAG = True


def main():
    pygame.init()
    game = Game()

    while not game.is_ended():
        game.update(game.FPS_CONTROLLER)
        game.render(game.GAME_WINDOW)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()