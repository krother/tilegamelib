
import time
import arcade
from tilegamelib.game import Game
from tilegamelib import TiledMap
from tilegamelib import MapMove
from tilegamelib import Vector
from tilegamelib.config import config


FRUITMAP = """##########
#b.#...aa#
##.#.#####
#h.#.e#.c#
##.#.##.##
##a#.#f..#
#*..b..#g#
##########"""

config.RESOLUTION = (450, 370)
config.TILE_FILE = 'fruit.csv'
config.GAME_NAME = "Collect Fruit"

FRUIT = 'abcdefgh'
EXIT_TILE = '*'
WALL_TILE = '#'


class CollectFruit(Game):

    def __init__(self):
        super().__init__()
        self.tm = TiledMap(self.tiles, FRUITMAP, offset=Vector(100, 100))
        self.pos = Vector(2, 1)

    def on_draw(self):
        arcade.start_render()
        self.tm.draw()
        px = self.tm.pos_in_pixels(self.pos)
        self.tiles['p'].draw(px.x, px.y, 32, 32)

    def move(self, vec):
        """starts a move"""
        dest = self.pos + vec
        field = self.tm.at(dest)
        if self.tm.at(dest) == '#':
            return
        self.pos = dest
        if field == EXIT_TILE:
            self.exit()
        elif field in FRUIT:
            self.tm.set(dest, '.')


if __name__ == '__main__':
    fruit = CollectFruit()
    arcade.run()
