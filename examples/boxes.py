
import time

import pygame
from pygame import Rect

from tilegamelib import TiledMap
from tilegamelib.game import Game
from tilegamelib.map_move import MapMove
from tilegamelib.sprites import Sprite
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


class Boxes:

    def __init__(self):
        self.game = Game()
        self.tm = TiledMap(self.game)
        self.player = Sprite(self.game, 'b.tail', (4, 1), speed=4)
        self.tm.set_map(BOXMAP)

    def draw(self):
        self.tm.draw()
        self.player.draw()

    def move(self, direction):
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
            moves = [self.player]
            if near in 'xX':
                # crate moved
                floor = '.' if near == 'x' else '*'
                insert = 'X' if far == '*' else 'x'
                moves.append(MapMove(self.tm, nearpos, direction, 4,
                          floor_tile=floor, insert_tile=insert))
            self.game.wait_for_move(moves, self.draw, 0.02)

        self.draw()
        self.check_complete()

    def check_complete(self):
        s = self.tm.get_map()
        if s.count('X') == 4:
            print("\nCongratulations!\n")
            time.sleep(2)
            self.game.exit()

    def run(self):
        self.game.event_loop(figure_moves=self.move, draw_func=self.draw)


if __name__ == '__main__':
    boxes = Boxes()
    boxes.run()
    pygame.quit()
