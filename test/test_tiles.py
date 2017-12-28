
import pygame
from pygame import Rect

from tilegamelib.tiles import Tile
from tilegamelib.vector import Vector
from util import TEST_GAME_CONTEXT


class TestTiles:

    def test_small_tile(self, tile_bitmap):
        """One small tile is displayed"""
        tile = Tile('dummy', Vector(0, 0), Vector(16, 16), tile_bitmap)
        dest = Rect(32, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()

    def test_big_tile(self, tile_bitmap):
        """One big tile is displayed"""
        tile = Tile('dummy', Vector(0, 0), Vector(32, 32), tile_bitmap)
        dest = Rect(132, 50, 32, 32)
        tile.draw(TEST_GAME_CONTEXT.screen, dest)
        pygame.display.update()
