from math import *
from typing import NamedTuple
from operator import itemgetter

class Vector(NamedTuple):
    angle: float
    norm: float

    def transform(self, other: Vector):
        sx = self.norm * cos(self.angle)
        sy = self.norm * sin(self.angle)

        ox = other.norm * cos(other.angle)
        oy = other.norm * sin(other.angle)

        nx = sx + ox
        ny = sy + oy

        return type(self)()