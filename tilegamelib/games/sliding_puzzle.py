"""
simple puzzle game:
arrange the fruits in rows
"""
import arcade
import os

from collections import Counter
from tilegamelib import TiledMap
from tilegamelib.tiled_map import AsciiMap, create_sprite
from tilegamelib.move import MapMove
from tilegamelib import Move
from tilegamelib import Vector
from tilegamelib import Game
from tilegamelib.config import config


PUZZLEMAP = """
######
#abce#
#ecba#
#abce#
#acb.#
######
"""

config.RESOLUTION = (350, 350)
config.BASE_PATH = os.path.split(__file__)[0] + os.sep
config.TILE_FILE = config.BASE_PATH + 'fruit.csv'
config.GAME_NAME = "Sliding Puzzle"



class SlidingPuzzle:
    """
    Sort equal items into rows
    """
    def __init__(self, box=PUZZLEMAP):
        self.box = AsciiMap(box)
        self.gap = self.find_gap()
         
    def __repr__(self):
        return str(self.box)

    def find_gap(self):
        for x in range(self.box.size.x):
            for y in range(self.box.size.y):
                pos = Vector(x, y)
                if self.box.at(pos) == '.':
                    return pos

    @staticmethod
    def count_same(row):
        """counts most frequent char in a string"""
        counter = Counter(row)
        return counter.most_common(1)[0][1]

    @property
    def solved(self):
        same = [self.count_same(row) for row in self.box.map[1:-1]]
        return sum(same) == 15

    def move(self, direction):
        source = self.gap - direction
        if self.box.at(source) != '#':
            self.gap = source
            return MapMove(self.box, source, direction)


class SlidingPuzzleGame(Game):

    def __init__(self, map_str=PUZZLEMAP):
        """initialize everything"""
        super().__init__()
        self.puzzle = SlidingPuzzle(map_str)
        self.map = TiledMap(self.tiles, self.puzzle.box, offset=Vector(100, 100))
        self.moving = None

    def on_draw(self):
        """automatically called to draw everything"""
        arcade.start_render()
        self.map.draw()
        if self.moving:
            self.moving.draw()

    def move(self, vec):
        """starts a move"""
        if self.moving:
            return
        move = self.puzzle.move(vec)
        self.map._cache_map()
        if move:
            sprite = create_sprite(
                self.tiles,
                move.char,
                self.map.pos_in_pixels(move.start_pos)
            )
            self.moving = Move(sprite, speed=2, move=move)

    def update(self, delta_time):
        """automatically called every frame"""
        if self.moving:
            self.moving.update()
            if self.moving.finished:
                self.moving = None
                self.map._cache_map()
                if self.puzzle.solved:
                    self.exit()


def main():
    window = SlidingPuzzleGame()
    arcade.run()


if __name__ == '__main__':
    main()
