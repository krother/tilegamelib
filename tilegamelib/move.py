
from .vector import RIGHT, ZERO_VECTOR, INVERSE_Y, Vector
from .config import config


class Move:
    """
    Moves a tile over a certain amount of steps in one direction.
    """
    def __init__(self, tile, start=ZERO_VECTOR, direction=RIGHT,
                 speed=1, on_finish=None):
        self.tile = tile
        self.pos = start
        self.speed = speed
        self.steps = config.TILE_SIZE
        self.direction = direction
        self.callback = on_finish

    @property
    def finished(self):
        return self.steps <= 0

    def update(self):
        if self.steps > 0:
            self.pos += self.direction * self.speed
            self.steps -= self.speed
        if self.steps <= 0:
            self.finish_move()

    def finish_move(self):
        if self.callback:
            self.callback()

    def draw(self):
        self.tile.draw(self.pos.x, self.pos.y, config.TILE_SIZE, config.TILE_SIZE)


class MapMove(Move):
    """
    Moves a tile on a map.
    First removes the tile, moves it and puts it back in a new position.
    Not that the tile does not exist on the map while moving.
    """
    def __init__(self, tmap, pos, direction, speed=2,
                 floor_tile='.', insert_tile=None,
                 on_finish=None):
        self.map = tmap
        self.end_pos = pos + direction
        self.tile_char = insert_tile or tmap.at(pos)

        super().__init__(self.map.get_tile(pos),
                         tmap.pos_in_pixels(pos), direction * INVERSE_Y,
                         speed=speed,
                         on_finish=on_finish)
        self.map.set(pos, floor_tile)

    def finish_move(self):
        self.map.set(self.end_pos, self.tile_char)
        super().finish_move()
