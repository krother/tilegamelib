
import time
import numpy as np

import pygame
from pygame import Rect

from .frame import Frame
from .move import Move, wait_for_move
from .screen import Screen
from .tile_factory import TileFactory
from .vector import DOWN, RIGHT, UP


class Sprite:
    """
    Object that moves along a tile grid.
    Sprites have a queue of moves.
    """
    def __init__(self, frame, tile, pos=None, speed=1):
        self.frame = frame
        self.tile = tile
        self.size = self.tile.size
        if pos is None:
            pos = (0, 0)
        self.pos = np.array(pos)  # position in tiles not pixels


        self.path = []  # Queue of moves
        self._move = None
        self.direction = None
        self.speed = speed
        self.callback = None

    def add_move(self, direction, priority=False, when_finished=None):
        """Adds a move to the movement queue."""
        if priority:
            self.path = [(direction, when_finished)] + self.path
        else:
            self.path.append((direction, when_finished))

    def get_next_move(self):
        """Pull next move from the queue"""
        if self.path:
            self.direction, when_finished = self.path.pop(0)
            self.callback = when_finished
            start_vector = self.pos * self.size
            self._move = Move(self.frame, self.tile, start_vector,
                self.direction * self.speed,
                steps=self.size[0] // self.speed,
                when_finished=self.finalize_move)

    @property
    def finished(self):
        if self._move and not self._move.finished or self.path:
            return False
        return True

    def move(self):
        """apply path to object vector and perform movement."""
        if not self._move:
            self.get_next_move()
        if self._move:
            self._move.move()

    def finalize_move(self):
        self.pos += self.direction
        self._move = None
        self.direction = None
        if self.callback:
            self.callback()
            self.callback = None

    def draw(self):
        """Draw the sprite on the screen."""
        if not self._move:
            pos = self.pos * self.size
            destrect = Rect(pos[0], pos[1], self.size[0], self.size[1])
            self.tile.draw(self.frame, destrect)
        else:
            self._move.draw()


if __name__ == '__main__':
    screen = Screen((800, 550), '../examples/data/background.png')
    frame = Frame(screen, Rect(64, 64, 400, 320))
    tile_factory = TileFactory('../examples/data/tiles.conf')

    sprite = Sprite(frame, tile_factory.get('#'), (3, 3))
    sprite.draw()
    pygame.display.update()
    time.sleep(1.0)

    sprite.add_move(DOWN)
    sprite.add_move(DOWN)
    sprite.add_move(RIGHT)
    sprite.add_move(UP)
    wait_for_move(sprite, screen, sprite.draw, 0.01)

    sprite.draw()
    pygame.display.update()
    time.sleep(1.0)
