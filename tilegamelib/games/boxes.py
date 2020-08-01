
import arcade
import os

from tilegamelib.game import Game
from tilegamelib import TiledMap
from tilegamelib import MapMove
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

config.RESOLUTION = (450, 400)
config.GAME_NAME = "Boxes"


class Boxes(Game):

    def __init__(self):
        super().__init__()
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
            self.exit()


def main():
    boxes = Boxes()
    arcade.run()


if __name__ == '__main__':
    main()
