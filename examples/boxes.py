
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
from pygame import Rect
from random import randint
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE
import pygame
import time

BOXMAP = """##########
#..#...**#
#..#.##**#
#..#.##..#
##x....x.#
#.x.....x#
#........#
##########"""

class Boxes:

    def __init__(self):
        self.screen = Screen(Vector(600, 400), 'data/background.png')
        self.frame = Frame(self.screen, Rect(64, 64, 320, 320))
        tile_factory = TileFactory('data/tiles.conf')
        self.tm = TiledMap(self.frame, tile_factory)
        self.player = Sprite(self.frame, tile_factory.get('b.tail'), Vector(4, 1), speed=2)
        self.tm.set_map(BOXMAP)
        self.draw()
        self.events = None

    def draw(self):
        self.tm.draw()
        self.player.draw()
        pygame.display.update()

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
            moves = MoveGroup()
            self.player.add_move(direction)
            moves.add(self.player)
            if near in 'xX':
                # crate moved
                floor = near=='x' and '.' or '*'
                insert = far=='*' and 'X' or 'x'
                moves.add(MapMove(self.tm, nearpos, direction, 1, floor_tile=floor, insert_tile=insert))

        wait_for_move(moves, self.screen, self.tm.draw, 0.01)

        self.tm.cache_map()
        self.draw()
        self.check_complete()

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

    def check_complete(self):
        s = self.tm.get_map()
        if s.count('X') == 4:
            print("\nCongratulations!\n")
            time.sleep(2)
            self.exit()

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
    boxes = Boxes()
    boxes.run()
            
