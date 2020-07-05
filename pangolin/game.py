from engine import Engine
import collections
import pygame
import vector
import entities
import components
import time
from vector import Vector

from pygame import gfxdraw


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
        self.engine = Engine(self)
        self.game_states_manager = GameStateManager()
        self.game_states_manager.start()
        while True:
            self.game_states_manager.handle_state_update()
            self.engine.update(delay)
            self.draw()
            delay = fps_clock.tick(self.fps)

    def start(self):
        self.start_pygame()

    # display
    def draw_entities(self, ents):
        for entity in ents:
            if not entity.has_comp(components.Drawable):
                continue
            self.draw_circle(
                self.screen,
                round(entity.pos.x),
                round(entity.pos.y),
                self.engine.get_entity_radius(entity.size),
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

    def kill(self, entity):
        self.entities.remove(entity)

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


class GameStateManager:
    def __init__(self):
        self.states = [0, 1]
        self.previous_state = self.states[0]

    def start(self):
        self.start = time.time()

    @property
    def state(self):
        return self.states[(int(time.time() - self.start) // 10) % len(self.states)]

    def handle_state_update(self):
        if self.previous_state == self.state:
            return

        self.previous_state = self.state
        if self.state == 1:
            # todo: add components to bubble entities so they can kill players
        elif self.state == 0:
            # todo: remove components to bubble so they can't kill players
        
