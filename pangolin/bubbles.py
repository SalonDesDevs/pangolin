from geometry import Vector


class Bubble:
    x: int
    y: int
    vel: Vector
    acc: Vector
    mass: int

    def __init__(self, x: int, y: int, vel: Vector, acc: Vector, mass: int):
        self._x = x
        self._y = y
        self.vel = vel
        self.acc = acc
        self._mass = mass

    @property
    def mass(self):
        return self._mass

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def move(self):
        pass

