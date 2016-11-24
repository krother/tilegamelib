#!/usr/bin/env python

from unittest import TestCase, main
from tilegamelib.tile_factory import TileFactory, NoTileError
from tilegamelib.tiles import Tile
from tilegamelib.vector import Vector
from test_data import TILE, TILE_SIZE, TILE_SPECS
from util import TEST_GAME_CONTEXT, showdoc
from pygame import Rect, image
import pygame


class TileTests(TestCase):

    @showdoc
    def test_small_tile(self):
        """One small tile is displayed"""
        bitmap = image.load(TILE).convert()
        tile = Tile('dummy', Vector(0, 0), Vector(16, 16), bitmap)
        dest = Rect(32, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()

    @showdoc
    def test_big_tile(self):
        """One big tile is displayed"""
        bitmap = image.load(TILE).convert()
        tile = Tile('dummy', Vector(0, 0), Vector(32, 32), bitmap)
        dest = Rect(132, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()


class TileFactoryTests(TestCase):

    def test_get_tiles(self):
        """Factory produces tiles."""
        tfac = TileFactory(TILE_SPECS)
        red = tfac.get('b.wall')
        self.assertTrue(isinstance(red, Tile))
        self.assertRaises(NoTileError, tfac.get, 'limegreen')
        # test synonyms
        self.assertTrue(isinstance(tfac.get('.'), Tile))
        self.assertTrue(isinstance(tfac.get('#'), Tile))
        self.assertTrue(isinstance(tfac.get('*'), Tile))
        self.assertTrue(isinstance(tfac.get('x'), Tile))

    @showdoc
    def test_display_tiles(self):
        """Display three tiles from factory"""
        screen = TEST_GAME_CONTEXT.screen
        tfac = TileFactory(TILE_SPECS)
        tfac.get('b.wall').draw(screen, Rect(32, 32, 32, 32))
        tfac.get('x').draw(screen, Rect(32, 64, 32, 32))
        tfac.get('*').draw(screen, Rect(64, 32, 32, 32))
        pygame.display.update()


if __name__ == "__main__":
    main()
