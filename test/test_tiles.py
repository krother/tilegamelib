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
from tilegamelib.vector import Vector
from test_settings import showdoc, TILE, TEST_GAME_CONTEXT, TILE_SIZE, TILE_SETS, TILE_SYNONYMS
from pygame import Rect, image
import pygame
import time

class TileTests(TestCase):

    @showdoc
    def test_small_tile(self):
        """One small tile is displayed"""
        bitmap = image.load(TILE).convert()
        tile = Tile('dummy', Vector(0,0), Vector(16,16), bitmap)
        dest = Rect(32, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()

    @showdoc
    def test_big_tile(self):
        """One big tile is displayed"""
        bitmap = image.load(TILE).convert()
        tile = Tile('dummy', Vector(0,0), Vector(32,32),bitmap)
        dest = Rect(132, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()


class TileFactoryTests(TestCase):

    def test_get_tiles(self):
        """Factory produces tiles."""
        tfac = TileFactory(TILE_SIZE, TILE_SETS, TILE_SYNONYMS)
        red = tfac.get('red')
        self.assertTrue(isinstance(red, Tile))
        self.assertRaises(NoTileError,tfac.get, 'limegreen')
        # test synonyms
        self.assertTrue(isinstance(tfac.get('.'), Tile))
        self.assertTrue(isinstance(tfac.get('r'), Tile))
        self.assertTrue(isinstance(tfac.get('g'), Tile))
        self.assertTrue(isinstance(tfac.get('b'), Tile))

    @showdoc
    def test_display_tiles(self):
        """Display three tiles from factory"""
        screen = TEST_GAME_CONTEXT.screen
        tfac = TileFactory(TILE_SIZE, TILE_SETS, TILE_SYNONYMS)
        tfac.get('blue').draw(screen, Rect(32, 32, 32, 32))
        tfac.get('r').draw(screen, Rect(32, 64, 32, 32))
        tfac.get('g').draw(screen, Rect(64, 32, 32, 32))
        pygame.display.update()

if __name__ == "__main__":
    main()
