
from screen import Screen
from frame import Frame
from tile_factory import TileFactory
from vector import Vector
from pygame import Rect
import pygame
import time


class AnimatedTile:
    """
    Loop through a sequence of tiles.
    """
    def __init__(self, tiles):
        self.tiles = tiles
        self.tile = None
        self.next_tile()

    @property
    def finished(self):
        if self.tiles:
            return False
        return True

    def next_tile(self):
        if not self.finished:
            self.tile = self.tiles.pop(0)

    def draw(self, frame, pos):
        self.tile.draw(frame, pos)



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
