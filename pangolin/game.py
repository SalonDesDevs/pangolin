import collections
import logging
import math
import random
import sys
import time

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
        self.last_projectile_time = 0

    def start_pygame(self):
        pygame.init()
        fps_clock = pygame.time.Clock()
        info_object = pygame.display.Info()
        self.screen_width = info_object.current_w
        self.screen_height = info_object.current_h
        self.scale = self.screen_height // 128

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.player = self.spawn_player(
            x=self.screen_width // 2,
            y=self.screen_height // 2,
            vel=vector.ZERO,
            acc=vector.ZERO,
            size=4,
            color=(255, 255, 255),
        )

        delay = 1 / self.fps  # delay is the time since last frame.
        while True:
            self.update(delay)
            self.draw()
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

        if key_pressed[pygame.K_q]:
            v = v.add(vector.LEFT)
        if key_pressed[pygame.K_d]:
            v = v.add(vector.RIGHT)
        if key_pressed[pygame.K_z]:
            v = v.add(vector.UP)
        if key_pressed[pygame.K_s]:
            v = v.add(vector.DOWN)

        # Player movement logic
        self.player.acc = Vector(1 if v.norm > 0.5 else 0, v.angle).add(
            self.player.vel.mul(-self.player.friction / self.player.mass)
        )

        if (
            pygame.mouse.get_pressed()[0]
            and time.time() - self.last_projectile_time > 1
        ):
            self.last_projectile_time = time.time()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            projectile_size = 0.5
            angle = Vector.from_xy(
                mouse_x - self.player.pos.x, mouse_y - self.player.pos.y
            ).angle

            projectile_shift = Vector(
                self.get_entity_radius(self.player.size)
                + self.get_entity_radius(projectile_size)
                + 1,
                angle,
            )

            projectile = self.spawn_projectile(
                x=self.player.pos.x + projectile_shift.x,
                y=self.player.pos.y + projectile_shift.y,
                vel=Vector(10, angle),
                size=projectile_size,
                color=(200, 50, 50),
            )

    def move_entities(self):
        for entity in self.entities:

            if not entity.has_comp(components.Moving):
                continue

            vel = (
                entity.vel.transform(entity.acc)
                if entity.has_comp(components.Movable)
                else entity.vel
            )
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
            WALL_RIGHT = self.screen_width - self.get_entity_radius(entity.size)
            WALL_LEFT = self.get_entity_radius(entity.size)
            WALL_BOTTOM = self.screen_height - self.get_entity_radius(entity.size)
            WALL_TOP = self.get_entity_radius(entity.size)

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

    def get_entity_radius(self, size):
        return round(size * self.scale)

    # display
    def draw_entities(self, ents):
        for entity in ents:
            if not entity.has_comp(components.Drawable):
                continue
            self.draw_circle(
                self.screen,
                round(entity.pos.x),
                round(entity.pos.y),
                self.get_entity_radius(entity.size),
                entity.color,
            )

    def draw_explosions(self, explosions):
        pass

    def draw_infos(self, power_info):
        pass

    # "low level"
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_entities(self.entities)
        self.draw_explosions(self.explosions)
        self.draw_infos(self.power_info)
        pygame.display.flip()

    def draw_circle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def spawn_bubble(self, entities, x, y, vel, size, color=None):
        bubble = entities.create_bubble(x, y, vel, size, color)
        self.entities.append(bubble)
        return bubble

    def spawn_player(self, x, y, vel, acc, size, color=None):
        player = entities.create_player(x, y, vel, acc, size, color)
        self.entities.append(player)
        return player

    def spawn_projectile(self, x, y, vel, size, color=None):
        projectile = entities.create_projectile(x, y, vel, size, color)
        self.entities.append(projectile)
        return projectile
