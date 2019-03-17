
import time

import arcade
from arcade.key import ESCAPE
from tilegamelib import TiledMap, load_tiles
from tilegamelib import MapMove
from tilegamelib import PLAYER_MOVES
from tilegamelib import Vector


FRUITMAP = """##########
#b.#...aa#
##.#.#####
#h.#.e#.c#
##.#.##.##
##a#.#f..#
#*..b..#g#
##########"""

SIZEX, SIZEY = (450, 370)

FRUIT = 'abcdefgh'
EXIT_TILE = '*'
WALL_TILE = '#'


class CollectFruit(arcade.Window):

    def __init__(self):
        super().__init__(SIZEX, SIZEY, "Collect Fruit")
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles = load_tiles('fruit.csv')
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
            arcade.window_commands.close_window()
        elif field in FRUIT:
            self.tm.set(dest, '.')

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        vec = PLAYER_MOVES.get(symbol)
        if vec:
            self.move(vec)
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()


if __name__ == '__main__':
    fruit = CollectFruit()
    arcade.run()
