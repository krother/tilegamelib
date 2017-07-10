
import time
from unittest import main
from unittest import TestCase

import pygame
from pygame import Rect

from test_settings import SHORT_DELAY
from test_settings import showdoc
from test_settings import TEST_GAME_CONTEXT
from tilegamelib.animation import AnimationSequence
from tilegamelib.frame import Frame
from tilegamelib.sprites import Sprite
from tilegamelib.vector import Vector


class AnimationTests(TestCase):

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40, 50, 160, 160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1, 1), speed=2)

    @showdoc
    def test_animation(self):
        """Animation of five colorful blocks"""
        tiles = [
            self.factory.get('g'),
            self.factory.get('b'),
            self.factory.get('r'),
            self.factory.get('b'),
            self.factory.get('g'),
            ]
        ani = AnimationSequence(self.frame, tiles, Vector(4,4), delay=5)
        while not ani.finished:
            ani.update()
            ani.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

if __name__ == "__main__":
    main()
