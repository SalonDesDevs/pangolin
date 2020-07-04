from geometry import Vector
import pygame
import logging

logger = logging.getLogger(__name__)

SPEED = 1

REST = Vector(0, 0)
UP = SPEED * Vector.from_xy(0, 1)
RIGHT = SPEED * Vector.from_xy(1, 0)
UP_RIGHT = SPEED * Vector.from_xy(1, 1)
UP_LEFT = SPEED * Vector.from_xy(-1, 1)
DOWN = -1 * UP
LEFT = -1 * RIGHT
DOWN_LEFT = -1 * UP_RIGHT
DOWN_RIGHT = -1 * UP_LEFT


class Entity:
    props = {}

    def __init__(self, *props):
        self.props = {}
        self.add_props(*props)

    def add_prop(self, prop):
        if len(self.props) > 32:
            logger.warning("TODO inject properties attributes inside")
        assert type(prop) not in self.props
        self.props[type(prop)] = prop

    def add_props(self, *props):
        for prop in props:
            self.add_prop(prop)

    def rem_prop(self, prop_cls):
        assert prop_cls in self.props
        del self.props[prop_cls]

    def has_prop(self, prop_cls):
        return prop_cls in self.props

    def __getattr__(self, attr):
        for prop in self.props:
            if hasattr(prop, attr):
                return prop.attr
        raise AttributeError(
            f"AttributeError: '{type(self).__name__}' object has no attribute '{attr}'"
        )

    def __setattr__(self, attr, value):
        for prop in self.props:
            if hasattr(prop, attr):
                prop.attr = value
    
    def __str__(self):
        return "entity with properties: " + ", ".join(prop.__name__ for prop in self.props)


def property(func):
    return func


@property
class Collidable:
    pos: Vector
    size: int

    def __init__(self, pos: Vector, size: int):
        self.pos = pos
        self.size = size

    @property
    def mass(self):
        return self.size ** 2


@property
class Moving:
    vel: Vector

    def __init__(self, vel: Vector):
        self.vel = vel


@property
class Movable:
    acc: Vector

    def __init__(self, acc: Vector):
        self.acc = acc


@property
class Colorful:
    color: tuple

    def __init__(self, color: tuple):
        self.color = color


@property
class Drawable:
    pass
