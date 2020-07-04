import pygame
import sys
from pygame.locals import *


class Game:
    def __init__(self):
        self.entities = []
        self.explosions = []
        self.power_info = 0

    # logic
    def update(self, delay):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # move entities
        for entity in self.entities:
            entity.move(delay)

    # display
    def draw_entities(self, screen, entities):
        pass

    def draw_explosions(self, screen, explosions):
        pass

    def draw_infos(self, screen, power_info):
        pass

    # "low level"
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.draw_entities(screen, self.entities)
        self.draw_explosions(screen, self.explosions)
        self.draw_infos(screen, self.power_info)
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
