#!/usr/bin/env python

import time

import pygame

from tilegamelib.config import config
from tilegamelib.sprite_list import SpriteList
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN, DOWNRIGHT, RIGHT


class TestSprites:
    """Tests for Sprite class"""
    def test_sprite_pos(self, game):
        """Sprite has a position."""
        sprite = Sprite(game, 'g', pos=(4, 3))
        assert sprite.pos == (4, 3)

    def move(self, sprite):
        """Moves sprite until movement terminates."""
        while sprite.is_moving:
            sprite.move()
            sprite.frame.clear()
            sprite.draw()
            pygame.display.update()
            time.sleep(config.SHORT_DELAY)

    def test_move_sprite(self, sprite):
        """Sprite moves east, then southeast."""
        sprite.add_move(RIGHT)
        sprite.add_move(DOWNRIGHT)
        self.move(sprite)
        assert sprite.pos == (3, 2)

    def test_priority_move_sprite(self, sprite):
        """Sprite moves southeast, then east."""
        sprite.add_move(RIGHT)
        sprite.add_move(DOWNRIGHT, True)
        self.move(sprite)


class SpriteListTests:

    def test_sprite_list(self, game):
        """Two sprites are moving."""
        sprites = SpriteList()
        s1 = Sprite(game, 'g', pos=(1, 0), speed=2)
        s2 = Sprite(game, 'b', pos=(1, 1), speed=4)
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
