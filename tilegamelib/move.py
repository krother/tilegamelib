
import time

import pygame
from pygame import Rect

from tilegamelib.frame import Frame
from .screen import Screen
from .tile_factory import TileFactory
from .vector import RIGHT, ZERO_VECTOR, Vector


class Move:
    """
    Moves a tile over a certain amount of steps in one direction.
    """
    def __init__(self, frame, tile, start_vector=ZERO_VECTOR, direction=RIGHT,
            steps=0, when_finished=None):
        self.frame = frame
        self.tile = tile
        self.start_vector = Vector(start_vector)
        self.current_vector = Vector(start_vector)
        self.steps = steps
        self.direction = direction
        self.finished = False
        self.callback = when_finished

    def move(self):
        if self.steps > 0:
            self.current_vector += self.direction
            self.steps -= 1
        if self.steps <= 0:
            self.finished = True
            if self.callback:
                self.callback()

    def draw(self):
        self.tile.draw(self.frame, self.current_vector)


if __name__ == '__main__':
    screen = Screen((800, 520), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 320, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')
    pac = tile_factory.get('b.pac_right')
    move = Move(frame, pac, (50, 50), RIGHT * 2, 200)
    wait_for_move(move, screen)
    time.sleep(1)
