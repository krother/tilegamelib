
from tilegamelib.vector import Vector


class TestVector:

    def test_vector(self):
        """Vector has x and y attributes."""
        a = Vector(1, 2)
        assert a.x == 1
        assert a.y == 2

    def test_set_xy(self):
        """x and y attributes can be set."""
        a = Vector(1, 2)
        a.x = 3
        a.y = 4
        assert a.x == 3
        assert a.y == 4

    def test_autocreate(self):
        """Creating a Vector from a Vector."""
        a = Vector(1, 2)
        b = Vector(a)
        assert b == a

    def test_add(self):
        """Vectors can be added."""
        a = Vector(1, 2)
        b = Vector(3, 4)
        c = a + b
        assert c.x == 4
        assert c.y == 6

    def test_add_tuple(self):
        """Tuples can be added to Vectors."""
        a = Vector(1, 2)
        b = (3, 4)
        c = a + b
        assert c.x == 4
        assert c.y == 6

    def test_multiply_scalar(self):
        """Vectors can be multiplied by numbers."""
        a = Vector(1, 2)
        c = a * 3
        assert c.x == 3
        assert c.y == 6

    def test_multiply_vec(self):
        """Vectors can be multiplied by Vectors."""
        a = Vector(1, 2)
        b = Vector(3, 4)
        c = a * b
        assert c.x == 3
        assert c.y == 8

    def test_floordiv(self):
        """Vectors can be divided."""
        a = Vector(3, 5)
        c = a // (1, 2)
        assert c.x == 3
        assert c.y == 2

    def test_iter(self):
        """Vectors can be iterated."""
        b = Vector(5, 6)
        assert list(b) == [5, 6]

    def test_equal(self):
        '''Vectors can be compared for equality'''
        a = Vector(1, 0)
        b = Vector(0, 1)
        c = Vector(1, 0)
        assert a == c
        assert a != b

    def test_equal_tuple(self):
        '''Vectors can be compared to tuples'''
        a = Vector(1, 0)
        assert a == (1, 0)
        assert a != (0, 1)

    def test_hashable(self):
        d = {Vector(1, 0): 'a',
             Vector(0, 1): 'b'
             }
        assert d[Vector(1, 0)] == 'a'
        assert d[Vector(0, 1)] == 'b'
