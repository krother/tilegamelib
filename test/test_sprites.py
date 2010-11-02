#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from tilegamelib.screen import Frame
from tilegamelib.sprites import Sprite, AnimationSequence, SpriteList
from test_settings import showdoc, SHORT_DELAY, TEST_GAME_CONTEXT
from unittest import TestCase, main
import numpy as np
import pygame
import time


class SpriteTests(TestCase):

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.frame = Frame(TEST_GAME_CONTEXT, (40,50), (160,160))
        self.sprite = Sprite(self.frame, self.factory.get('g'), speed=2)

    def test_sprite_pos(self):
        sprite = Sprite(self.frame, self.factory.get('g'), pos=(4,3))
        self.assertEqual(sprite.pos[0], 4)
        self.assertEqual(sprite.pos[1], 3)

    @showdoc
    def test_move_sprite(self):
        """Sprite moves east, then southeast."""
        self.sprite.add_move(np.array([1,0]))
        self.sprite.add_move(np.array([1,1]))
        while self.sprite.is_moving():
            self.sprite.move()
            self.frame.clear()
            self.sprite.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

    @showdoc
    def test_priority_move_sprite(self):
        """Sprite moves southeast, then east."""
        self.sprite.add_move(np.array([1,0]))
        self.sprite.add_priority_move(np.array([1,1]))
        while self.sprite.is_moving():
            self.sprite.move()
            self.frame.clear()
            self.sprite.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

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
        ani = AnimationSequence(self.frame, tiles, np.array([4,4]), delay=5)
        while not ani.finished:
            ani.update()
            ani.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

    @showdoc
    def test_sprite_list(self):
        """Two sprites are moving."""
        sprites = SpriteList()
        s1 = Sprite(self.frame, self.factory.get('g'), pos=np.array([1,0]), speed=2)
        s2 = Sprite(self.frame, self.factory.get('b'), pos=np.array([1,1]), speed=4)
        sprites.append(s1)
        sprites.append(s2)
        s1.add_move(np.array([1,0]))
        s1.add_move(np.array([0,1]))
        s2.add_move(np.array([0,1]))
        while sprites.is_moving():
            sprites.update()
            self.frame.clear()
            sprites.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

if __name__ == "__main__":
    main()
