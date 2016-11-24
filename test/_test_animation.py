
from tilegamelib.vector import Vector
from tilegamelib.frame import Frame
from tilegamelib.sprites import Sprite
from tilegamelib.animation import AnimationSequence
from test_settings import showdoc, SHORT_DELAY, TEST_GAME_CONTEXT
from unittest import TestCase, main
from pygame import Rect
import pygame
import time


class AnimationTests(TestCase):

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40,50, 160,160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1,1), speed=2)

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
