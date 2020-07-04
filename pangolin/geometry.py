from math import *
from typing import NamedTuple

class Vector(NamedTuple):
    angle: float
    norm: float

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

    def __mul__(self, x):
        return type(self).from_xy(self.x * x, self.y * x)
