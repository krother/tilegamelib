
from tilegamelib import Screen, Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener
from tilegamelib.map_move import MapMove
from tilegamelib.move import Move, wait_for_move
from tilegamelib.move_group import MoveGroup
from tilegamelib.sprites import Sprite
from tilegamelib.draw_timer import draw_timer
from pygame import Rect
from random import randint
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

        wait_for_move(moves, self.screen, self.draw, 0.01)

        self.tm.cache_map()
        self.draw()
        self.check_complete()

    def check_complete(self):
        s = self.tm.get_map()
        if s.count('X') == 4:
            print("\nCongratulations!\n")
            time.sleep(2)
            self.exit()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):     
            self.events.event_loop()


if __name__ == '__main__':
    boxes = Boxes()
    boxes.run()
            
