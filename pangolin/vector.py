from math import *
from typing import NamedTuple
import logging

logger = logging.getLogger(__name__)


class Vector(NamedTuple):
    norm: float
    angle: float

    def transform(self, other: "Vector"):
        return self.from_xy(self.x + other.x, self.y + other.y)

    @property
    def x(self):
        return self.norm * cos(self.angle)

    @property
    def y(self):
        return self.norm * sin(self.angle)

    @classmethod
    def from_xy(cls, x, y):
        return cls(sqrt(x ** 2 + y ** 2), atan2(y, x))

    def mul(self, x):
        offset = pi if x < 0 else 0
        return type(self)(self.norm * abs(x), self.angle + offset)

    def add(self, other):
        return type(self).from_xy(self.x + other.x, self.y + other.y)

    def __str__(self):
        return (f"{type(self).__name__}("
                f"norm={self.norm:.2f}, "
                f"angle={self.angle:.5f}, "
                f"x={self.x:.2f}, "
                f"y={self.y:.2f})")


SPEED = 1
ZERO = Vector(0, 0)
DOWN = Vector.from_xy(0, 1).mul(SPEED)
RIGHT = Vector.from_xy(1, 0).mul(SPEED)
UP = DOWN.mul(-1)
LEFT = RIGHT.mul(-1)
