
import pygame
from pygame import image
from pygame import Rect

from test.conftest import TILE
from tilegamelib.tiles import Tile
from tilegamelib.vector import Vector
from util import showdoc
from util import TEST_GAME_CONTEXT


class TestTiles:

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
