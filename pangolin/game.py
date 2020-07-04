import pygame
import sys
from pygame.locals import *


class Game:

    # logic
    def update(self, delay):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    # display
    def draw_bubbles(screen):
        pass

    def draw_animations(screen):
        pass

    def draw_infos(screen):
        pass

    # "low level"
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_bubbles(screen)
        pygame.display.flip()

    def start_pygame(self):
        pygame.init()
        fps = 60.0
        fps_clock = pygame.time.Clock()
        info_object = pygame.display.Info()
        screen = pygame.display.set_mode((info_object.current_w, info_object.current_h))

        delay = 1 / fps  # delay is the time since last frame.
        while True:
            self.update(delay)
            self.draw(screen)
            delay = fps_clock.tick(fps)

    def start(self):
        self.start_pygame()
