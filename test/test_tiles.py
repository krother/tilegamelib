
from tilegamelib.tiles import Tile
from tilegamelib.vector import Vector
from data import TILE
from util import TEST_GAME_CONTEXT, showdoc
import pytest
from pygame import Rect, image
import pygame


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
