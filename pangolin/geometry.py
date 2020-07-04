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
