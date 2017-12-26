
from collections import Counter

import pygame
from pygame import Rect

from tilegamelib import Game, TiledMap, Vector
from tilegamelib.map_move import MapMove
from tilegamelib.config import config


PUZZLEMAP = """######
#abce#
#ecba#
#abce#
#acb.#
######"""

config.RESOLUTION = (350, 350)


class SlidingPuzzle:

    def __init__(self):
        self.game = Game()
        self.tm = TiledMap(self.game)
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
        self.game.wait_for_move(move, self.tm.draw, 0.01)
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
            self.game.exit()

    def run(self):
        self.game.event_loop(figure_moves=self.move)


if __name__ == '__main__':
    puzzle = SlidingPuzzle()
    puzzle.run()
    pygame.quit()
