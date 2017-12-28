
from .move import Move
from .vector import Vector


class MapMove:
    """
    Moves a tile on a map.
    """
    def __init__(self, tmap, pos, direction, speed=1, floor_tile=None, insert_tile=None):
        self.map = tmap
        pos = Vector(pos)
        self.end_pos = pos + direction
        self.tile_char = insert_tile or tmap.at(pos)

        tile = self.map.get_tile(pos)
        self._move = Move(tmap.frame, tile, tmap.pos_in_pixels(pos),
                          direction * 2, steps=16)
        self.map.set_tile(pos, floor_tile or '.')

    @property
    def finished(self):
        return self._move.finished

    def move(self):
        self._move.move()
        if self._move.finished:
            self.finish_move()

    def draw(self):
        self._move.draw()

    def finish_move(self):
        self.map.set_tile(self.end_pos, self.tile_char)
