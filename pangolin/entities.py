from geometry import Vector
import pygame
import logging

logger = logging.getLogger(__name__)

SPEED = 1

UP = SPEED * Vector.from_xy(0, 1)
RIGHT = SPEED * Vector.from_xy(1, 0)
UP_RIGHT = SPEED * Vector.from_xy(1, 1)
UP_LEFT = SPEED * Vector.from_xy(-1, 1)
DOWN = -UP
LEFT = -RIGHT
DOWN_LEFT = -UP_RIGHT
DOWN_RIGHT = -UP_LEFT


class Bubble:
    pos: Vector
    vel: Vector
    acc: Vector
    size: int

    def __init__(self, pos: Vector, vel: Vector, acc: Vector, mass: int):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def mass(self):
        return self.size ** 2

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def move(self):
        self.vel = self.vel.transform(self.acc)
        self.pos = self.pos.transform(self.vel)

    def collide(self, other: Bubble):
        pass


class BubbleEntity(Bubble):
    color: tuple

    def __init__(
        self, x: int, y: int, vel: Vector, acc: Vector, size: int, color: tuple
    ):
        super().__init__(x, y, vel, acc, size)
        self._color = color

    @property
    def color(self):
        return self._color

    def draw(self, screen, scale):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size * scale)


class Player(Bubble):
    K = 10

    def move(self):
        cls = type(self)
        friction = -cls.K * Vector.from_xy(self.vel.x, self.vel.y)
        self.acc = self.acc.transform(friction)
        super().move()


