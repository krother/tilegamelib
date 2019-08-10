
import time
import arcade
from arcade.key import ESCAPE
from tilegamelib import TiledMap, load_tiles
from tilegamelib import MapMove
from tilegamelib import PLAYER_MOVES
from tilegamelib import Vector
from tilegamelib.sprites import TileSprite
from tilegamelib.config import config


BOXMAP = """##########
#..#...**#
#..#.##**#
#..#.##..#
##x....x.#
#.x.....x#
#........#
##########"""

SIZEX, SIZEY = (450, 400)


class Boxes(arcade.Window):

    def __init__(self):
        super().__init__(SIZEX, SIZEY, "Collect Fruit")
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles = load_tiles('fruit.csv')
        self.tm = TiledMap(self.tiles, BOXMAP, offset=Vector(96, 96))
        self.player = TileSprite(self.tiles['b.tail'], (4, 1), speed=4, offset=Vector(96, 320))
        self.moves = None

    def on_draw(self):
        self.tm.draw()
        self.player.draw()
        if self.moves and len(self.moves) > 1:
            self.moves[1].draw()

    def move(self, direction):
        if self.moves:
            return
        nearpos = self.player.pos + direction
        farpos = nearpos + direction
        near = self.tm.at(nearpos)
        far = self.tm.at(farpos)
        if near == '#':
            return
        if near in 'xX' and far in '#xX':
            return
        else:
            # move possible
            self.player.add_move(direction)
            self.moves = [self.player]
            if near in 'xX':
                # crate moved
                floor = '.' if near == 'x' else '*'
                insert = 'X' if far == '*' else 'x'
                self.moves.append(MapMove(self.tm, nearpos, direction, 4,
                          floor_tile=floor, insert_tile=insert))

    def update(self, time_delta):
        if self.moves:
            for m in self.moves:
                m.update()
            if self.moves[0].finished:
                self.moves = None
                self.check_complete()

    def check_complete(self):
        s = self.tm.get_map()
        if s.count('X') == 4:
            print("\nCongratulations!\n")
            time.sleep(2)
            arcade.window_commands.close_window()

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        vec = PLAYER_MOVES.get(symbol)
        if vec:
            self.move(vec)
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()


if __name__ == '__main__':
    boxes = Boxes()
    arcade.run()
