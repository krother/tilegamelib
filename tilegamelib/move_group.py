
import time

import pygame
from pygame import Rect

from .frame import Frame
from .map_move import MapMove
from .move import wait_for_move
from .screen import Screen
from .tile_factory import TileFactory
from .tiled_map import TiledMap
from .vector import DOWN
from .vector import LEFT
from .vector import RIGHT
from .vector import UP
from .vector import Vector


class MoveGroup:
    """
    Moves multiple items simultaneously
    """
    def __init__(self):
        self.moves = []

    def add(self, move):
        self.moves.append(move)

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


if __name__ == '__main__':
    fruitmap = """############
#..aa..bb..#
#..aa..bb..#
#cc..dd..ee#
#cc..dd..ee#
#..ff..gg..#
#..ff..gg..#
############"""

    screen = Screen(Vector(800, 550), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 400, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')
    tm = TiledMap(frame, tile_factory)

    tm.set_map(fruitmap)
    tm.draw()
    pygame.display.update()

    mg = MoveGroup()
    mg.add(MapMove(tm, Vector(5, 3), LEFT * 2, 2))
    mg.add(MapMove(tm, Vector(6, 3), LEFT * 2, 2))
    mg.add(MapMove(tm, Vector(5, 4), LEFT * 2, 2))
    mg.add(MapMove(tm, Vector(6, 4), LEFT * 2, 2))

    wait_for_move(mg, screen, tm.draw, 0.02)

    mg = MoveGroup()
    mg.add(MapMove(tm, Vector(7, 5), RIGHT, 2))
    mg.add(MapMove(tm, Vector(8, 5), DOWN, 2))
    mg.add(MapMove(tm, Vector(7, 6), UP, 2))
    mg.add(MapMove(tm, Vector(8, 6), LEFT, 2))

    wait_for_move(mg, screen, tm.draw, 0.02)

    tm.draw()
    pygame.display.update()
    time.sleep(1.0)
