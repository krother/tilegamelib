
import time
from random import randint

import pygame
from pygame import Rect

from .frame import Frame
from .move import Move, wait_for_move
from .screen import Screen
from .tile_factory import TileFactory
from .tiled_map import TiledMap
from .vector import DOWN, LEFT, RIGHT, UP, Vector


class MapMove:
    """
    Moves a tile on a map.
    """
    def __init__(self, tmap, pos, direction, speed=1, floor_tile=None, insert_tile=None):
        self.map = tmap
        self.end_pos = pos + direction
        self.tile_char = insert_tile or tmap.at(pos)

        tile = self.map.get_tile(pos)
        self._move = Move(tmap.frame, tile, tmap.pos_in_pixels(pos),
                          direction * 2, steps=16)
        self.map.set_tile(pos, floor_tile or '.')
        self.map.cache_map()

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
        self.map.cache_map()


if __name__ == '__main__':
    fruitmap = """############
#..aa..bb..#
#..aa..bb..#
#cc..dd..ee#
#cc..dd..ee#
#..ff..gg..#
#..ff..gg..#
############"""

    screen = Screen()
    frame = Frame(screen, Rect(64, 64, 400, 320))
    tile_factory = TileFactory()
    tm = TiledMap(frame, tile_factory)

    tm.set_map(fruitmap)
    tm.draw()
    pygame.display.update()

    for i in range(40):
        move = None
        while move is None:
            pos = Vector(randint(1, 10), randint(1, 6))
            direction = [UP, DOWN, LEFT, RIGHT][randint(0, 3)]
            newpos = pos + direction
            if tm.at(pos) != '.' and tm.at(newpos) != '#':
                move = MapMove(tm, pos, direction, 2)
        wait_for_move(move, screen, tm.draw, 0.01)

    tm.draw()
    pygame.display.update()
    time.sleep(1.0)
