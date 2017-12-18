#!/usr/bin/env python

import time

import pygame
from pygame import Rect

from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.sprite_list import SpriteList
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import DOWNRIGHT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import Vector
from util import showdoc
from util import TEST_GAME_CONTEXT


class SpriteTests:

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40, 50, 160, 160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1, 1), speed=2)

    def test_sprite_pos(self):
        """Sprite has a position."""
        sprite = Sprite(self.frame, self.factory.get('g'), pos=Vector(4, 3))
        self.assertEqual(sprite.pos.x, 4)
        self.assertEqual(sprite.pos.y, 3)

    def move(self):
        """Moves sprite until movement terminates."""
        while self.sprite.is_moving():
            self.sprite.move()
            self.frame.clear()
            self.sprite.draw()
            pygame.display.update()
            time.sleep(config.SHORT_DELAY)

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


class SpriteListTests:

    def setUp(self):
        self.factory = TEST_GAME_CONTEXT.tile_factory
        self.tile = self.factory.get('g')
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(40, 50, 160, 160))
        self.sprite = Sprite(self.frame, self.tile, Vector(1, 1), speed=2)

    @showdoc
    def test_sprite_list(self):
        """Two sprites are moving."""
        sprites = SpriteList()
        s1 = Sprite(self.frame, self.factory.get('g'), pos=Vector(1, 0), speed=2)
        s2 = Sprite(self.frame, self.factory.get('b'), pos=Vector(1, 1), speed=4)
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
            time.sleep(config.SHORT_DELAY)
