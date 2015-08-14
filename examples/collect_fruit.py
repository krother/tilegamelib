
from tilegamelib.screen import Screen
from tilegamelib.frame import Frame
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT
from tilegamelib.map_move import MapMove
from tilegamelib.move import Move, wait_for_move
from tilegamelib.move_group import MoveGroup
from tilegamelib.sprites import Sprite
from tilegamelib.events import EventGenerator
from tilegamelib.event_listener import EventListener
from tilegamelib.game import Game
from pygame import Rect
from random import randint
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE
import pygame
import time

FRUITMAP = """##########
#b.#...aa#
##.#.#####
#h.#.e#.c#
##.#.##.##
##a#.#f..#
#*..b..#g#
##########"""

class CollectFruit:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory('data/tiles.conf')
        self.tm = TiledMap(self.frame, tile_factory)
        self.player = Sprite(self.frame, tile_factory.get('b.tail'), Vector(4, 1), speed=2)
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
        if near == '#': 
            return
        self.player.add_move(direction)
        wait_for_move(self.player, self.screen, self.tm.draw, 0.01)
        self.check_player_square()

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field == '*':
            time.sleep(1)
            self.exit()
        elif field in 'abcdefgh':
            self.score += 100
            self.tm.set_tile(self.player.pos, '.')
            self.tm.cache_map()
            self.draw()

    def up(self):
        self.move(UP)

    def down(self):
        self.move(DOWN)

    def left(self):
        self.move(LEFT)

    def right(self):
        self.move(RIGHT)

    def exit(self):
        self.events.exit_signalled()

    def run(self):
        self.events = EventGenerator()
        listener = EventListener(keymap = {
            K_LEFT: self.left,
            K_RIGHT: self.right,
            K_UP: self.up,
            K_DOWN: self.down,
            K_ESCAPE: self.exit
            })
        self.events.add_listener(listener)
        self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/collect_fruit.conf', CollectFruit)
    game.run()

