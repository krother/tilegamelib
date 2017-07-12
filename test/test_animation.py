
import time

import pygame
from pygame import Rect

from tilegamelib.animation import AnimatedTile
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.vector import Vector
from util import TEST_GAME_CONTEXT, showdoc


class AnimationTests:

    @showdoc
    def test_animation(self):
        """Animation of five colorful blocks"""
        factory = TEST_GAME_CONTEXT.tile_factory
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40, 50, 160, 160))
        tiles = [factory.get(x) for x in "abcdefgh"]

        ani = AnimatedTile(tiles, factory, frame, Vector(4, 4), delay=5)
        while not ani.finished:
            ani.draw(frame, Rect(64, 64, 32, 32))
            pygame.display.update()
            time.sleep(config.SHORT_DELAY)
            ani.next_tile()
