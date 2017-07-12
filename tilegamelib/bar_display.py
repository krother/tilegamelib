
import time

import pygame
from pygame import Rect

from tilegamelib.frame import Frame
from tilegamelib.screen import Screen
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiled_map import TiledMap


class BarDisplay:

    def __init__(self, frame, tile_factory, value, tile_name, vertical=False):
        self.frame = frame
        self.map = TiledMap(frame, tile_factory)
        self.value = value
        self.tile_name = tile_name
        self.vertical = vertical
        self.redraw()

    def redraw(self):
        if self.vertical:
            self.map.set_map('\n'.join([self.tile_name] * self.value))
        else:
            self.map.set_map(self.tile_name * self.value)
        self.frame.clear()
        self.map.draw()

    def increase(self):
        self.value += 1
        self.redraw()

    def decrease(self):
        if self.value > 0:
            self.value -= 1
        self.redraw()


if __name__ == '__main__':
    screen = Screen()
    tile_factory = TileFactory()
    frame = Frame(screen, Rect(96, 64, 640, 32))
    bananas = BarDisplay(frame, tile_factory, 0, 'b', False)
    frame = Frame(screen, Rect(64, 64, 32, 320))
    cherries = BarDisplay(frame, tile_factory, 10, 'c', True)
    for i in range(15):
        pygame.display.update()
        time.sleep(0.1)
        # screen.clear()
        bananas.increase()
        cherries.decrease()
        pygame.display.update()
    for i in range(15):
        pygame.display.update()
        time.sleep(0.1)
        screen.clear()
        bananas.decrease()
        cherries.increase()
        pygame.display.update()
    time.sleep(2)
