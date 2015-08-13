#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT, UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT
from tilegamelib.frame import Frame
from tilegamelib.sprites import Sprite, SpriteList
from test_settings import showdoc, SHORT_DELAY, TEST_GAME_CONTEXT
from unittest import TestCase, main
from pygame import Rect
import pygame
import time


class SpriteTests(TestCase):

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40,50, 160,160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1,1), speed=2)

    def test_sprite_pos(self):
        """Sprite has a position."""
        sprite = Sprite(self.frame, self.factory.get('g'), pos=Vector(4,3))
        self.assertEqual(sprite.pos.x, 4)
        self.assertEqual(sprite.pos.y, 3)

    def move(self):
        """Moves sprite until movement terminates."""
        while self.sprite.is_moving():
            self.sprite.move()
            self.frame.clear()
            self.sprite.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

    @showdoc
    def test_move_sprite(self):
        """Sprite moves east, then southeast."""
        self.sprite.add_move(RIGHT)
        self.sprite.add_move(DOWNRIGHT)
        self.move()
        self.assertEqual(self.sprite.pos.x, 3)
        self.assertEqual(self.sprite.pos.y, 2)

    @showdoc
    def test_priority_move_sprite(self):
        """Sprite moves southeast, then east."""
        self.sprite.add_move(RIGHT)
        self.sprite.add_move(DOWNRIGHT, True)
        self.move()


class SpriteListTests(TestCase):

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40,50, 160,160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1,1), speed=2)
    
    @showdoc
    def test_sprite_list(self):
        """Two sprites are moving."""
        sprites = SpriteList()
        s1 = Sprite(self.frame, self.factory.get('g'), pos=Vector(1,0), speed=2)
        s2 = Sprite(self.frame, self.factory.get('b'), pos=Vector(1,1), speed=4)
        sprites.append(s1)
        sprites.append(s2)
        s1.add_move(RIGHT)
        s1.add_move(DOWN)
        s2.add_move(DOWN)
        while sprites.is_moving():
            sprites.update()
            self.frame.clear()
            sprites.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

if __name__ == "__main__":
    main()
