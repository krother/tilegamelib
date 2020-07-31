"""
simple puzzle game:
arrange the fruits in rows
"""
import arcade
import os

from collections import Counter
from tilegamelib import TiledMap
from tilegamelib import MapMove
from tilegamelib import Vector
from tilegamelib import Game
from tilegamelib.config import config


PUZZLEMAP = """######
#abce#
#ecba#
#abce#
#acb.#
######"""

config.RESOLUTION = (350, 350)
config.BASE_PATH = os.path.split(__file__)[0] + os.sep
config.TILE_FILE = config.BASE_PATH + 'fruit.csv'
config.GAME_NAME = "Sliding Puzzle"


class SlidingPuzzle(Game):
    """Sort equal items into rows"""
    def __init__(self):
        """initialize everything"""
        super().__init__()
        self.map = TiledMap(self.tiles, PUZZLEMAP, offset=Vector(100, 100))
        self.gap = Vector(4, 4)
        self.moving = None

    @staticmethod
    def count_same(row):
        """counts most frequent char in a string"""
        counter = Counter(row)
        return counter.most_common(1)[0][1]

    def check_complete(self):
        """exit if all fruit sorted into rows"""
        same = [self.count_same(row) for row in self.map.map[1:5]]
        if sum(same) == 15:
            self.exit()

    def on_draw(self):
        """automatically called to draw everything"""
        arcade.start_render()
        self.map.draw()
        if self.moving:
            self.moving.draw()

    def move(self, vec):
        """starts a move"""
        source = self.gap - vec
        if self.map.at(source) == '#' or self.moving:
            return
        self.moving = MapMove(self.map, source, vec)
        self.gap = source

    def update(self, delta_time):
        """automatically called every frame"""
        if self.moving:
            self.moving.update()
            if self.moving.finished:
                self.moving = None
                self.check_complete()


def main():
    window = SlidingPuzzle()
    arcade.run()


if __name__ == '__main__':
    main()
