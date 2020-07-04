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


class Entity:
    props: dict

    def __init__(self):
        self.props = {}

    def add_prop(self, prop):
        if len(self.props) > 32:
            logger.warning("TODO inject properties attributes inside")
        assert type(prop) not in self.props
        self.props[type(prop)] = prop

    def rem_prop(self, prop_cls):
        assert prop_cls in self.props
        del self.props[prop_cls]

    def has_prop(self, prop_cls):
        return prop_cls in self.props

    def __getattr__(self, attr):
        for prop in self.properties:
            if hasattr(prop, attr):
                return prop.attr
        raise AttributeError(f"AttributeError: '{type(self).__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        for prop in self.properties:
            if hasattr(prop, attr):
                prop.attr = value


def property(func):
    return func


@property
class Odooable:
    pos: Vector
    size: int

    def __init__(self, pos: Vector, size: int):
        self.pos = pos
        self.size = size

    @property
    def mass(self):
        return self.size ** 2
    
@property
class Mouving:
    vel: Vector

    def __init__(self, vel: Vector):
        self.vel = vel

@property
class Mouvable:
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
