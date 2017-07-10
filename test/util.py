"""
Helper functions for testing
"""

import time

import pygame
from pygame import Rect

from data import BACKGROUND_IMAGE
from data import RESOLUTION
from data import TILE_SPECS
from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import TileFactory
from tilegamelib.basic_boxes import TextBox


class TestGameContext:

    def __init__(self):
        pygame.init()
        self.screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        self.tile_factory = TileFactory(TILE_SPECS)


TEST_GAME_CONTEXT = TestGameContext()

DELAY = 0.01
SHORT_DELAY = 0.05
VERY_SHORT_DELAY = 0.02


def next_frame():
    pygame.display.update()
    time.sleep(DELAY)


def showdoc(func):
    """
    decorator function showing a docstring
    """
    def do_show(self):
        """Clear screen, show docstring, run test."""
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(10, 400, 400, 50))
        tb = TextBox(frame, func.__doc__)
        tb.draw()
        pygame.display.update()
        func(self)
        next_frame()
    return do_show


def graphictest(func):
    """
    decorator function updating display and waiting
    """
    def wrap_test(self):
        func(self)
        next_frame()

    return wrap_test
