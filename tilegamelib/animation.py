
from .screen import Screen
from .frame import Frame
from .tile_factory import TileFactory
from .vector import Vector
from pygame import Rect
import pygame
import time


class AnimatedTile:
    """
    Loop through a sequence of tiles.
    """
    def __init__(self, tiles, tile_factory, frame, pos, delay=5):
        self.tiles = list(tiles)
        self.tile_factory = tile_factory
        self.frame = frame
        self.pos = pos * 32
        self.tile = None
        self.delay_max = delay
        self.delay = 0
        self.move()

    @property
    def finished(self):
        if self.tiles or self.delay > 0:
            return False
        return True

    def move(self):
        if not self.finished:
            if self.delay == 0:
                tile = self.tiles.pop(0)
                self.tile = self.tile_factory.get(tile)
                self.delay = self.delay_max
            else:
                self.delay -= 1
            self.draw()

    def draw(self):
        self.tile.draw(self.frame, self.pos)



if __name__ == '__main__':
    screen = Screen(Vector(800,550), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 400, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')
    tiles = [tile_factory.get(x) for x in "abcdefgh"]
    ani = AnimatedTile(tiles)
    
    while not ani.finished:
        screen.clear()
        ani.draw(frame, Rect(64, 64, 32, 32))
        pygame.display.update()
        time.sleep(0.5)
        ani.next_tile()

    ani.draw(frame, Rect(64, 64, 32, 32))
    pygame.display.update()
    time.sleep(1.0)
