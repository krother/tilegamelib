
import time

import pygame

from tilegamelib.animation import AnimatedTile
from tilegamelib.config import config
from tilegamelib.vector import Vector


class TestAnimation:

    def test_animation(self, tile_factory, frame):
        """Animation of five colorful blocks"""
        ani = AnimatedTile("abcde", tile_factory, frame, Vector(4, 4), delay=3)
        while not ani.finished:
            ani.draw()
            pygame.display.update()
            time.sleep(config.SHORT_DELAY)
            ani.move()
