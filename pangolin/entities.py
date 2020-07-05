import logging
import math
import pygame
import colors
import components
from vector import Vector

logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, *comps):
        super().__setattr__("comps", {})
        self.add_comps(*comps)

    def add_comp(self, comp):
        if len(self.comps) > 32:
            logger.warning("TODO inject component attributes inside")
        assert type(comp) not in self.comps, f"{comp} already in {self}"
        self.comps[type(comp)] = comp

    def add_comps(self, *comps):
        for comp in comps:
            self.add_comp(comp)

    def rem_comp(self, comp_cls):
        assert comp_cls in self.comps
        del self.comps[comp_cls]

    def has_comp(self, comp_cls):
        return comp_cls in self.comps

    def __getattr__(self, attr):
        for comp in self.comps.values():
            if hasattr(comp, attr):
                return getattr(comp, attr)
        raise AttributeError(f"AttributeError: {self} has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        for comp in self.comps.values():
            if hasattr(comp, attr):
                setattr(comp, attr, value)

    def __str__(self):
        comps = ", ".join(comp.__name__ for comp in self.comps)
        return f"<{type(self).__name__} ({comps})>"


def create_bubble(x, y, vel, size, color):
    if not color:
        color = random.choice(colors.all_colors)

    return Entity(
        components.Collidable(Vector.from_xy(x, y), size),
        components.Drawable(),
        components.Moving(vel),
        components.Colorful(color),
    )


def create_player(x, y, vel, acc, size, color):
    FRICTION = 1
    if not color:
        color = random.choice(colors.all_colors)

    return Entity(
        components.Collidable(Vector.from_xy(x, y), size),
        components.Drawable(),
        components.Moving(vel),
        components.Colorful(color),
        components.Movable(acc, FRICTION),
    )


def create_projectile(x, y, vel, size, color):
    if not color:
        color = random.choice(colors.all_colors)

    return Entity(
        components.Collidable(Vector.from_xy(x, y), size),
        components.Drawable(),
        components.Moving(vel),
        components.Colorful(color),
    )
