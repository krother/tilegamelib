
from .move import Move
from .vector import Vector, INVERSE_Y


class TileSprite:
    """
    Object that moves along a tile grid.
    Sprites have a queue of moves.
    """
    def __init__(self, tile, pos=(0, 0), speed=1, offset=Vector(0, 0)):
        self.tile = tile
        self.pos = Vector(pos)  # position in tiles not pixels

        self.path = []  # Queue of moves
        self._move = None
        self.direction = None
        self.speed = speed
        self.callback = None
        self.offset = offset
        self.size = 32

    def add_move(self, direction, priority=False, when_finished=None):
        """Adds a move to the movement queue."""
        if priority:
            self.path = [(direction, when_finished)] + self.path
        else:
            self.path.append((direction, when_finished))

    def get_next_move(self):
        """Pull next move from the queue"""
        if self.path:
            self.direction, when_finished = self.path.pop(0)
            self.callback = when_finished
            start = self.get_pos_in_pixels()
            self._move = Move(self.tile, start,
                self.direction*INVERSE_Y,
                speed=self.speed,
                on_finish=self.finalize_move,
                )

    @property
    def is_moving(self):
        return not self.finished

    @property
    def finished(self):
        if self._move and not self._move.finished or self.path:
            return False
        return True

    def update(self):
        """apply path to object vector and perform movement."""
        if not self._move:
            self.get_next_move()
        if self._move:
            self._move.update()

    def finalize_move(self):
        self.pos += self.direction
        self._move = None
        self.direction = None
        if self.callback:
            self.callback()
            self.callback = None

    def get_pos_in_pixels(self):
        """Returns the screen position in pixels (x,y)"""
        pixelpos = Vector(self.pos.x * 32, -self.pos.y * 32)
        return pixelpos + self.offset

    def draw(self):
        """Draw the sprite on the screen."""
        if not self._move:
            px = self.get_pos_in_pixels()
            self.tile.draw(px.x, px.y, 32, 32)
        else:
            self._move.draw()
