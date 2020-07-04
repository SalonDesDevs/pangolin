from geometry import Vector
import pygame


class Bubble:
    x: int
    y: int
    vel: Vector
    acc: Vector
    size: int

    def __init__(self, x: int, y: int, vel: Vector, acc: Vector, size: int):
        self._x = x
        self._y = y
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
        return self._x

    @property
    def y(self):
        return self._y

    def move(self):
        pass


class BubbleEntity(Bubble):
    x: int
    y: int
    vel: Vector
    acc: Vector
    size: int

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
