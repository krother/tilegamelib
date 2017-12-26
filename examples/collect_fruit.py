
import time

import pygame
from pygame import Rect

from tilegamelib import TiledMap
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
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

FRUIT = 'abcdefgh'
EXIT_TILE = '*'
WALL_TILE = '#'


class CollectFruit:

    def __init__(self):
        self.game = Game()
        self.tm = TiledMap(self.game)
        self.player = Sprite(self.game, 'b.pac_right', (4, 1), speed=4)
        self.tm.set_map(FRUITMAP)
        self.draw()
        self.events = None
        self.score = 0

    def draw(self):
        self.player.move()
        self.tm.draw()
        self.player.draw()
        self.check_player_square()

    def move(self, direction):
        if self.player.finished:
            nearpos = self.player.pos + direction
            near = self.tm.at(nearpos)
            if near == WALL_TILE:
                return
            self.player.add_move(direction)

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field == EXIT_TILE:
            self.game.exit()
        elif field in FRUIT:
            self.score += 100
            self.tm.set_tile(self.player.pos, '.')

    def run(self):
        self.game.event_loop(figure_moves=self.move, draw_func=self.draw)



if __name__ == '__main__':
    fruit = CollectFruit()
    fruit.run()
    time.sleep(1)
