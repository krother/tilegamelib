
from pygame import Rect

from tilegamelib.vector import Vector


class VectorTests:

    def test_vector(self):
        """Vector has x and y attributes."""
        a = Vector(1, 2)
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 2)

    def test_add(self):
        """Vectors can be added."""
        a = Vector(1, 2)
        b = Vector(3, 4)
        c = a + b
        self.assertEqual(c.x, 4)
        self.assertEqual(c.y, 6)

    def test_mul(self):
        """Vectors can be multiplied."""
        a = Vector(1, 2)
        c = a * 3
        self.assertEqual(c.x, 3)
        self.assertEqual(c.y, 6)

    def test_rect(self):
        """Vectors can be used for creating Rect objects."""
        a = Vector(0, 0)
        b = Vector(5, 6)
        r = Rect(a.x, a.y, b.x, b.y)
        self.assertEqual(r.x, 0)
        self.assertEqual(r.y, 0)
        self.assertEqual(r.width, 5)
        self.assertEqual(r.height, 6)

    def test_iter(self):
        """Vectors can be iterated."""
        b = Vector(5, 6)
        self.assertEqual(list(b), [5, 6])

    def test_equal(self):
        '''Vectors can be compared for equality'''
        a = Vector(1, 0)
        b = Vector(0, 1)
        c = Vector(1, 0)
        self.assertEqual(a, c)
        self.assertNotEqual(a, b)

    def test_hashable(self):
        d = {Vector(1, 0): 'a',
             Vector(0, 1): 'b'
             }
        self.assertEqual(d[Vector(1, 0)], 'a')
        self.assertEqual(d[Vector(0, 1)], 'b')
