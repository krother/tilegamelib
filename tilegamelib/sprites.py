
from pygame import Rect

from .move import Move
from .vector import Vector


class Sprite:
    """
    Object that moves along a tile grid.
    Sprites have a queue of moves.
    """
    def __init__(self, game, tile_name, pos=(0, 0), speed=1, frame=None):
        self.frame = frame or game.frame
        self.tile = game.get_tile(tile_name)
        self.size = self.tile.size
        self.pos = Vector(pos)  # position in tiles not pixels

        self.path = []  # Queue of moves
        self._move = None
        self.direction = None
        self.speed = speed
        self.callback = None

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
            start_vector = self.pos * self.size
            self._move = Move(self.frame, self.tile, start_vector,
                self.direction * self.speed,
                steps=self.size.x // self.speed,
                when_finished=self.finalize_move)

    @property
    def is_moving(self):
        return not self.finished

    @property
    def finished(self):
        if self._move and not self._move.finished or self.path:
            return False
        return True

    def move(self):
        """apply path to object vector and perform movement."""
        if not self._move:
            self.get_next_move()
        if self._move:
            self._move.move()

    def finalize_move(self):
        self.pos += self.direction
        self._move = None
        self.direction = None
        if self.callback:
            self.callback()
            self.callback = None

    def draw(self):
        """Draw the sprite on the screen."""
        if not self._move:
            pos = self.pos * self.size
            destrect = Rect(pos.x, pos.y, self.size.x, self.size.y)
            self.tile.draw(self.frame, destrect)
        else:
            self._move.draw()
