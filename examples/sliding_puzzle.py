
from collections import Counter

import pygame
from pygame import Rect

from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib import Vector
from tilegamelib.event_listener import FigureMoveListener
from tilegamelib.events import EventGenerator
from tilegamelib.map_move import MapMove
from tilegamelib.move import wait_for_move
from tilegamelib.config import config


PUZZLEMAP = """######
#abce#
#ecba#
#abce#
#acb.#
######"""

config.RESOLUTION = Vector(350, 350)

class SlidingPuzzle:

    def __init__(self):
        self.screen = Screen()
        frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory()
        self.tm = TiledMap(frame, tile_factory)
        self.gap = Vector(4, 4)
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

    def get_same(self, row):
        counter = Counter(row)
        return counter.most_common(1)[0][1]

    def check_complete(self):
        s = self.tm.get_map()
        rows = s.split('\n')
        same = [self.get_same(row) for row in rows[1:5]]
        if sum(same) == 15:
            print("\nCongratulations!\n")
            self.events.exit_signalled()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.event_loop()


if __name__ == '__main__':
    puzzle = SlidingPuzzle()
    puzzle.run()
    pygame.quit()
