import logging
import math
import random
import sys
import time
import pygame
import vector
from vector import Vector
from pygame.locals import *

import components


logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, game):
        self.game = game
        self.last_projectile_time = 0

    @property
    def player(self):
        return self.game.player

    @property
    def entities(self):
        return self.game.entities

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

            projectile = self.game.spawn_projectile(
                x=self.player.pos.x + projectile_shift.x,
                y=self.player.pos.y + projectile_shift.y,
                vel=Vector(10, angle),
                size=projectile_size,
                color=(200, 50, 50),
            )

    def move_entities(self):
        collide_funcs = []

        def collision(func):
            collide_funcs.append(func)
            return func

        @collision
        def bounce():
            """Multi-wall bouncing algorithm"""
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
            nonlocal pos, vel

            # bounce the entity a bit futher the wall so we ensure
            # we don't bounce back back in the same wall and get stuck
            bounce = entity.vel.norm  # + vector.SPEED

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
                return False  # didn't bounced
            return True  # bounced

        @collision
        def collide():
            """Multi-entity bouncing / hitting algorithm"""
            return False

        for entity in self.entities:

            if not entity.has_comp(components.Moving):
                continue

            vel = (
                entity.vel.transform(entity.acc)
                if entity.has_comp(components.Movable)
                else entity.vel
            )
            pos = entity.pos.transform(vel)

            WALL_RIGHT = self.game.screen_width - self.get_entity_radius(entity.size)
            WALL_LEFT = self.get_entity_radius(entity.size)
            WALL_BOTTOM = self.game.screen_height - self.get_entity_radius(entity.size)
            WALL_TOP = self.get_entity_radius(entity.size)

            for i in range(16):  # watchdog
                if not any(collide_func() for collide_func in collide_funcs):
                    break
            else:
                logger.warning("{entity} bounced on too many walls")
                self.kill(entity)

            entity.vel = vel
            entity.pos = pos

    def get_entity_radius(self, size):
        return round(size * self.game.scale)
