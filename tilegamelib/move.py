
from tilegamelib import RIGHT, ZERO_VECTOR, INVERSE_Y, Vector
from .config import config


class BasicMove:
    """
    Represents move of an element from A to B.
    
    The purpose of moves is to animate tiles smoothly
    without the game objects knowing about the graphics engine
    """
    def __init__(self, char, start_pos, direction, on_finish=None):
        self.char = char
        self.start_pos = start_pos
        self.direction = direction
        self.end_pos = start_pos + direction
        self.callback = on_finish

    def finish(self):
        if self.callback:
            self.callback()


class MapMove(BasicMove):
    """
    Moves a tile on a 2D map.
    First removes the tile, moves it and puts it back in a new position.
    Note that the tile does not exist on the map while moving.
    """
    def __init__(self, ascii_map, pos, direction,
                 floor_tile='.', insert_tile=None,
                 on_finish=None):
        self.map = ascii_map
        self.tile_char = insert_tile or self.map.at(pos)

        super().__init__(self.map.at(pos),
                         pos, direction,
                         on_finish=on_finish)
        self.map.set(pos, floor_tile)

    def finish(self):
        self.map.set(self.end_pos, self.tile_char)
        super().finish()



class Move:
    """
    Moves a tile over a certain amount of steps in one direction.
    """
    def __init__(self, tile=None, start=ZERO_VECTOR, direction=RIGHT,
                 speed=1, on_finish=None, move=None):
        self.tile = tile
        self.pos = start
        self.speed = speed
        self.steps = config.TILE_SIZE
        if move:
            self.move = move
        else:
            self.move = BasicMove('*', start, direction, on_finish)

    @property
    def finished(self):
        return self.steps <= 0

    def update(self):
        if self.steps > 0:
            self.pos += self.move.direction * self.speed
            self.steps -= self.speed
        if self.steps <= 0:
            self.move.finish()

    def draw(self):
        self.tile.draw(self.pos.x, self.pos.y, config.TILE_SIZE, config.TILE_SIZE)


# class MapMove:
#     """
#     Moves a tile on a map.
#     First removes the tile, moves it and puts it back in a new position.
#     Note that the tile does not exist on the map while moving.
#     """
#     def __init__(self, tmap, pos, direction, speed=2,
#                  floor_tile='.', insert_tile=None,
#                  on_finish=None):
#         self.map = tmap
#         self.end_pos = pos + direction
#         self.tile_char = insert_tile or tmap.at(pos)

#         super().__init__(self.map.get_tile(pos),
#                          tmap.pos_in_pixels(pos), direction * INVERSE_Y,
#                          speed=speed,
#                          on_finish=on_finish)
#         self.map.set(pos, floor_tile)

#     def finish_move(self):
#         self.map.set(self.end_pos, self.tile_char)
#         super().finish_move()


class MoveGroup:
    """
    Moves multiple items simultaneously
    """
    def __init__(self, moves):
        self.moves = moves

    @property
    def finished(self):
        for m in self.moves:
            if not m.finished:
                return False
        return True

    def move(self):
        for m in self.moves:
            m.move()

    def draw(self):
        for m in self.moves:
            m.draw()

    def __repr__(self):
        return "<MoveGroup with {} moves, finished: {}>".format(len(self.moves), self.finished)
