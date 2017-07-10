
from tilegamelib import Screen, Frame, TileFactory, Vector, TiledMap
from tilegamelib.map_move import MapMove
from tilegamelib.move import wait_for_move
from tilegamelib.events import EventGenerator
from tilegamelib.event_listener import FigureMoveListener
from tilegamelib.util import DATA_PATH
from pygame import Rect
from collections import Counter
import pygame

PUZZLEMAP = """######
#abce#
#ecba#
#abce#
#acb.#
######"""


class SlidingPuzzle:

    def __init__(self):
        self.screen = Screen(Vector(350, 350), DATA_PATH + 'background.png')
        frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory(DATA_PATH + 'tiles.conf')
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
