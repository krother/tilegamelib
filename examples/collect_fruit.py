
import time

import pygame
from pygame import Rect

from tilegamelib import TiledMap
from tilegamelib.game import Game
from tilegamelib.move import wait_for_move
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
        tf = self.game.tile_factory
        self.tm = TiledMap(self.game.frame, tf)
        self.player = Sprite(self.game.frame, tf.get('b.pac_right'), (4, 1), speed=4)
        self.tm.set_map(FRUITMAP)
        self.draw()
        self.events = None
        self.score = 0

    def draw(self):
        self.tm.draw()
        self.player.draw()
        pygame.display.update()

    def move(self, direction):
        nearpos = self.player.pos + direction
        near = self.tm.at(nearpos)
        if near == WALL_TILE:
            return
        self.player.add_move(direction)
        wait_for_move(self.player, self.game.screen, self.draw, 0.01)
        self.check_player_square()

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field == EXIT_TILE:
            time.sleep(1)
            self.game.exit()
        elif field in FRUIT:
            self.score += 100
            self.tm.set_tile(self.player.pos, '.')
            self.draw()

    def run(self):
        self.game.event_loop(figure_moves=self.move, draw_func=self.draw)


if __name__ == '__main__':
    fruit = CollectFruit()
    fruit.run()
