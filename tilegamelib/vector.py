

class Vector:

    def __init__(self, x, y):
        self.coord = (x, y)

    @property
    def x(self):
        return self.coord[0]

    @property
    def y(self):
        return self.coord[1]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, number):
        x = self.x * number
        y = self.y * number
        return Vector(x, y)

    def __iter__(self):
        return self.coord.__iter__()

    def __eq__(self, other):
        if type(other) == type(self):
            if self.x == other.x and self.y == other.y:
                return True

    def __hash__(self):
        return str(self).__hash__()

    # def __cmp__(self, other):
    #     return cmp(str(self), str(other))

    def __repr__(self):
        return '[%i;%i]' % (self.x, self.y)

# direction vectors for various moves
UP = Vector(0, -1)
DOWN = Vector(0, 1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)
UPLEFT = Vector(-1, -1)
DOWNLEFT = Vector(-1, 1)
UPRIGHT = Vector(1, -1)
DOWNRIGHT = Vector(1, 1)
