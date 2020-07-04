import pygame
import sys
import logging
import random
import entities
import collections
from geometry import Vector
from pygame.locals import *
from pygame import gfxdraw

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, fps):
        self.COLORS = [
            (227, 102, 93),
            (111, 227, 93),
            (93, 164, 227),
            (160, 93, 227),
            (227, 93, 169),
        ]
        self.bubbles_by_color = collections.defaultdict(list)
        self.entities = []
        self.explosions = []
        self.power_info = 0
        self.fps = fps

    # logic
    def spawn_bubble(self, x, y, vel, size, color=None):
        if not color:
            color = random.choice(self.COLORS)
        bubble = entities.Entity(
            entities.Collidable(Vector.from_xy(x, y), size),
            entities.Drawable(),
            entities.Moving(vel),
            entities.Colorful(color),
        )
        self.bubbles_by_color[color].append(bubble)
        self.entities.append(bubble)
        return bubble

    def spawn_player(self, x, y, vel, acc, size, color=None):
        if not color:
            color = random.choice(self.COLORS)
        player = entities.Entity(
            entities.Collidable(Vector.from_xy(x, y), size),
            entities.Drawable(),
            entities.Moving(vel),
            entities.Colorful(color),
            entities.Movable(acc, 1),
        )
        self.entities.append(player)
        return player

    def update(self, delay):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        self.handle_keystrokes()
        self.move_entities()

    def handle_keystrokes(self):
        key_pressed = pygame.key.get_pressed()
        v = entities.REST

        if key_pressed[pygame.K_LEFT]:
            v = v.add(entities.LEFT)
        if key_pressed[pygame.K_RIGHT]:
            v = v.add(entities.RIGHT)
        if key_pressed[pygame.K_UP]:
            v = v.add(entities.UP)
        if key_pressed[pygame.K_DOWN]:
            v = v.add(entities.DOWN)

        self.player.acc = Vector(1 if v.norm > 0.5 else 0, v.angle).add(
            self.player.vel.mul(-self.player.friction / self.player.mass)
        )

    def move_entities(self):
        for entity in self.entities:
            if entity.has_prop(entities.Moving):
                entity.vel = entity.vel.transform(entity.acc)
                entity.pos = entity.pos.transform(entity.vel)

    # display
    def draw_entities(self, screen, ents):
        for entity in ents:
            if not entity.has_prop(entities.Drawable):
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

    def start_pygame(self):
        pygame.init()
        fps_clock = pygame.time.Clock()
        info_object = pygame.display.Info()
        screen_width = info_object.current_w
        screen_height = info_object.current_h
        self.scale = screen_height // 128

        screen = pygame.display.set_mode((screen_width, screen_height))

        self.player = self.spawn_player(
            x=screen_width // 2,
            y=screen_height // 2,
            vel=entities.REST,
            acc=entities.REST,
            size=4,
            color=(255, 255, 255),
        )

        delay = 1 / self.fps  # delay is the time since last frame.
        while True:
            self.update(delay)
            self.draw(screen)
            delay = fps_clock.tick(self.fps)

    def start(self):
        self.start_pygame()
