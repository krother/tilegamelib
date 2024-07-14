
from typing import Type, Union, Tuple, Iterable, NewType


class Vector:
    """
    Direction vectors for moves, positions etc.

    Vector objects can be used for simple arithmetics,
    like adding positions to each other.

    They are hashable, unlike NumPy arrays.
    """
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vector):
                self.coord = args[0].coord
            else:  # tuple or similar
                self.coord = args[0]
        elif len(args) == 2:  # x, y
            self.coord = tuple(args)
        else:
            assert False

    @property
    def x(self) -> int:
        return self.coord[0]

    @x.setter
    def x(self, x: int):
        self.coord = (x, self.y)

    @property
    def y(self) -> int:
        return self.coord[1]

    @y.setter
    def y(self, y: int):
        self.coord = (self.x, y)

    def __add__(self, other: Union['Vector', Tuple[int, int]]) -> 'Vector':
        """return sum of two vectors"""
        if not isinstance(other, Vector):
            other = Vector(other)
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other: Union['Vector', Tuple[int, int]]) -> 'Vector':
        """return difference of two vectors"""
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, other: Union['Vector', Tuple[int, int]]) -> 'Vector':
        """return product of two vectors"""
        if isinstance(other, int):
            x = self.x * other
            y = self.y * other
        else:
            if not isinstance(other, Vector):
                other = Vector(other)
            x = self.x * other.x
            y = self.y * other.y
        return Vector(x, y)

    def __floordiv__(self, other: Union['Vector', Tuple[int, int]]) -> 'Vector':
        """divides two vectors"""
        if isinstance(other, int):
            x = self.x // other
            y = self.y // other
        else:
            if not isinstance(other, Vector):
                other = Vector(other)
            x = self.x // other.x
            y = self.y // other.y
        return Vector(x, y)

    def __iter__(self) -> Iterable:
        return self.coord.__iter__()

    def __eq__(self, other) -> bool:
        if type(other) == type(self):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return Vector(self) == Vector(other)

    def __hash__(self) -> int:
        return str(self).__hash__()

    def __repr__(self) -> str:
        return '[%i;%i]' % (self.x, self.y)


ZERO_VECTOR = Vector(0, 0)
UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)
UPLEFT = Vector(-1, -1)
DOWNLEFT = Vector(-1, 1)
UPRIGHT = Vector(1, -1)
DOWNRIGHT = Vector(1, 1)
INVERSE_Y = Vector(1, -1)  # because inverted y-axis in arcade
