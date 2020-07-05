import abc
from collections import defaultdict
from vector import Vector


class Component(metaclass=abc.ABCMeta):
    pass


class Collidable(Component):
    pos: Vector
    size: int

    def __init__(self, pos: Vector, size: int):
        self.pos = pos
        self.size = size

    @property
    def mass(self):
        return self.size ** 2


class Moving(Component):
    vel: Vector

    def __init__(self, vel: Vector):
        self.vel = vel


class Movable(Component):
    acc: Vector
    friction: float

    def __init__(self, acc: Vector, friction: float = 0):
        self.acc = acc
        self.friction = friction


class Colorful(Component):
    color: tuple

    def __init__(self, color: tuple):
        self.color = color


class Drawable(Component):
    pass


class Identifiable(Component):
    name: str
    ident: int

    counts = defaultdict(int)

    def __init__(self, name: str):
        self.name = name
        self.ident = type(self).counts[name]
        type(self).counts[name] = type(self).counts[name] + 1 & 0xFFFF
