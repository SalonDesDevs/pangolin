from geometry import Vector
import math
import pygame
import logging

logger = logging.getLogger(__name__)

SPEED = 1

REST = Vector(0, 0)
DOWN = Vector.from_xy(0, 1).mul(SPEED)
UP = DOWN.mul(-1)
RIGHT = Vector.from_xy(1, 0).mul(SPEED)
LEFT = RIGHT.mul(-1)


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
        for prop in self.props.values():
            if hasattr(prop, attr):
                return getattr(prop, attr)
        raise AttributeError(
            f"AttributeError: '{type(self).__name__}' object has no attribute '{attr}'"
        )

    def __setattr__(self, attr, value):
        for prop in self.props.values():
            if hasattr(prop, attr):
                setattr(prop, attr, value)
    
    def __str__(self):
        return "entity with properties: " + ", ".join(prop.__name__ for prop in self.props)


def component(func):
    return func


@component
class Collidable:
    pos: Vector
    size: int

    def __init__(self, pos: Vector, size: int):
        self.pos = pos
        self.size = size

    @property
    def mass(self):
        return self.size ** 2


@component
class Moving:
    vel: Vector

    def __init__(self, vel: Vector):
        self.vel = vel


@component
class Movable:
    acc: Vector
    friction: float

    def __init__(self, acc: Vector, friction: float = 0):
        self.acc = acc
        self.friction = friction

@component
class Colorful:
    color: tuple

    def __init__(self, color: tuple):
        self.color = color


@component
class Drawable:
    pass
