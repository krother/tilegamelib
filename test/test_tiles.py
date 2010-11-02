#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from unittest import TestCase, main
from tilegamelib.tiles import Tile, TileFactory, NoTileError
from test_settings import showdoc, TILE, TEST_GAME_CONTEXT
import pygame
import time

class TileTests(TestCase):

    @showdoc
    def test_tile(self):
        """One tile is displayed"""
        bitmap = pygame.image.load(TILE).convert()
        tile = Tile('dummy',(1,1),(16,16),bitmap)
        dest = pygame.Rect(32, 16, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()

class TileFactoryTests(TestCase):

    def test_get_tiles(self):
        """Factory produces tiles."""
        tf = TileFactory(TEST_GAME_CONTEXT.settings)
        red = tf.get('red')
        self.assertTrue(isinstance(red,Tile))
        self.assertRaises(NoTileError,tf.get,'limegreen')
        # test synonyms
        self.assertTrue(isinstance(tf.get('.'),Tile))
        self.assertTrue(isinstance(tf.get('r'),Tile))
        self.assertTrue(isinstance(tf.get('g'),Tile))
        self.assertTrue(isinstance(tf.get('b'),Tile))

    @showdoc
    def test_display_tiles(self):
        """Display three tiles from factory"""
        scr = TEST_GAME_CONTEXT.screen
        tf = TileFactory(TEST_GAME_CONTEXT.settings)
        tf.get('blue').draw(scr, pygame.Rect(32, 32, 32, 32))
        tf.get('r').draw(scr, pygame.Rect(32, 64, 32, 32))
        tf.get('g').draw(scr, pygame.Rect(64, 32, 32, 32))
        pygame.display.update()

if __name__ == "__main__":
    main()
