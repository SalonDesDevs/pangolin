import collections
import logging
import math
import random
import sys

import pygame
from pygame.locals import *
from pygame import gfxdraw

import components
import entities
import vector
from vector import Vector

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, fps):
        self.bubbles_by_color = collections.defaultdict(list)
        self.entities = []
        self.explosions = []
        self.power_info = 0
        self.fps = fps

    def start_pygame(self):
        pygame.init()
        fps_clock = pygame.time.Clock()
        info_object = pygame.display.Info()
        self.screen_width = info_object.current_w
        self.screen_height = info_object.current_h
        self.scale = self.screen_height // 128

        screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.player = entities.spawn_player(
            x=self.screen_width // 2,
            y=self.screen_height // 2,
            vel=vector.ZERO,
            acc=vector.ZERO,
            size=4,
            color=(255, 255, 255),
        )
        self.entities.append(self.player)

        delay = 1 / self.fps  # delay is the time since last frame.
        while True:
            self.update(delay)
            self.draw(screen)
            delay = fps_clock.tick(self.fps)

    def start(self):
        self.start_pygame()

    # logic
    def update(self, delay):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        self.handle_keystrokes()
        self.move_entities()

    def handle_keystrokes(self):
        key_pressed = pygame.key.get_pressed()
        v = vector.ZERO

        if key_pressed[pygame.K_LEFT]:
            v = v.add(vector.LEFT)
        if key_pressed[pygame.K_RIGHT]:
            v = v.add(vector.RIGHT)
        if key_pressed[pygame.K_UP]:
            v = v.add(vector.UP)
        if key_pressed[pygame.K_DOWN]:
            v = v.add(vector.DOWN)

        # Player movement logic
        self.player.acc = Vector(1 if v.norm > 0.5 else 0, v.angle).add(
            self.player.vel.mul(-self.player.friction / self.player.mass)
        )

    def move_entities(self):
        for entity in self.entities:
            if not entity.has_comp(components.Moving):
                continue

            vel = entity.vel.transform(entity.acc)
            pos = entity.pos.transform(vel)

            # Multi-wall bouncing algorithm
            #
            #    wall
            #     |
            # O------>0
            #  \  |  /
            #   \ | /
            #    \|/
            #     |
            #    /|
            #   O |
            #
            WALL_RIGHT = self.screen_width - entity.size
            WALL_LEFT = entity.size
            WALL_BOTTOM = self.screen_height - entity.size
            WALL_TOP = entity.size

            # bounce the entity a bit futher the wall so we ensure
            # we don't bounce back back in the same wall and get stuck
            bounce = entity.vel.norm + vector.SPEED

            for i in range(16):  # watchdog
                if pos.x > WALL_RIGHT:
                    vel = Vector(bounce, math.pi - entity.vel.angle)
                    pos = Vector.from_xy(2 * WALL_RIGHT - pos.x, pos.y).transform(vel)

                elif pos.x < WALL_LEFT:
                    vel = Vector(bounce, math.pi - entity.vel.angle)
                    pos = Vector.from_xy(2 * WALL_LEFT - pos.x, pos.y).transform(vel)

                elif pos.y > WALL_BOTTOM:
                    vel = Vector(bounce, -entity.vel.angle)
                    pos = Vector.from_xy(pos.x, 2 * WALL_BOTTOM - pos.y).transform(vel)

                elif pos.y < WALL_TOP:
                    vel = Vector(bounce, -entity.vel.angle)
                    pos = Vector.from_xy(pos.x, 2 * WALL_TOP - pos.y).transform(vel)

                else:
                    # base case, the entity didn't cross a wall
                    break
            else:
                raise RuntimeError("Bounced on too many walls")

            entity.vel = vel
            entity.pos = pos

    # display
    def draw_entities(self, screen, ents):
        for entity in ents:
            if not entity.has_comp(components.Drawable):
                continue
            self.draw_circle(
                screen,
                round(entity.pos.x),
                round(entity.pos.y),
                entity.size * self.scale,
                entity.color,
            )

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

    def draw_circle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

