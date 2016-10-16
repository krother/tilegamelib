
from tilegamelib.screen import Screen
from tilegamelib.frame import Frame
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT
from tilegamelib.map_move import MapMove
from tilegamelib.move import wait_for_move
from tilegamelib.events import EventGenerator
from tilegamelib.event_listener import EventListener
from pygame import Rect
from random import randint
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE
from collections import Counter
import pygame
import time

PUZZLEMAP = """######
#abcd#
#dcba#
#abcd#
#acb.#
######"""

class SlidingPuzzle:

    def __init__(self):
        self.screen = Screen(Vector(350, 350), 'data/background.png')
        frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory('data/tiles.conf')
        self.tm = TiledMap(frame, tile_factory)
        self.gap = Vector(4,4)
        self.tm.set_map(PUZZLEMAP)
        self.tm.draw()
        self.events = None
        pygame.display.update()

    def move(self, direction):
        start = self.gap - direction
        if self.tm.at(start) == '#':
            return
        move = MapMove(self.tm, start, direction, 2)
        wait_for_move(move, self.screen, self.tm.draw, 0.01)
        self.gap = start
        self.check_complete()

    def up(self):
        self.move(UP)

    def down(self):
        self.move(DOWN)

    def left(self):
        self.move(LEFT)

    def right(self):
        self.move(RIGHT)

    def exit(self):
        self.events.exit_signalled()

    def get_same(self, row):
        counter = Counter(row)
        return counter.most_common(1)[0][1]

    def check_complete(self):
        s = self.tm.get_map()
        rows = s.split('\n')
        same = [self.get_same(row) for row in rows[1:5]]
        if sum(same) == 15:
            print("\nCongratulations!\n")
            self.exit()

    def run(self):
        self.events = EventGenerator()
        listener = EventListener(keymap = {
            K_LEFT: self.left,
            K_RIGHT: self.right,
            K_UP: self.up,
            K_DOWN: self.down,
            K_ESCAPE: self.exit
            })
        self.events.add_listener(listener)
        self.events.event_loop()


if __name__ == '__main__':
    puzzle = SlidingPuzzle()
    puzzle.run()
