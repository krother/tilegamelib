#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

import pygame
import pygame.font
from tilegamelib.settings import DialogSettings
from tilegamelib.interfaces import GameContext
from tilegamelib.tiles import TileFactory
from tilegamelib.screen import Screen, Frame
from tilegamelib.basic_boxes import TextBox
import time

class TestSettings(DialogSettings):
    """
    Parameters for Frutris
    """
    RESOLUTION = (800,550)
    BACKGROUND_IMAGE = 'test_data/background.png'
    TITLE_IMAGE = 'test_data/test_tile.png'
    BOX_IMAGE = 'test_data/test_tile.png'

    # fonts
    pygame.font.init()
    DEMIBOLD_BIG = pygame.font.Font('test_data/LucidaSansDemiBold.ttf',20)
    DEMIBOLD_SMALL = pygame.font.Font('test_data/LucidaSansDemiBold.ttf',14)

    # high score window
    HIGHSCORE_FILE = 'test_data/test_scores.txt'
    HIGHSCORE_IMAGE = 'test_data/test_tile.png'

    GAME_OVER_DELAY = 1000

    # tiles
    TILE_SETS = [('test_data/boxes.png','test_data/tiles.spec')]
    TILE_SYNONYMS = [
                    ('.','empty'),
                    ('r','red'),
                    ('b','blue'),
                    ('g','green'),
                    ('#','cursor'),
                    ]

    KEY_EVENT_QUEUE = [27]



class TestGameContext(GameContext):

    def __init__(self):
        GameContext.__init__(self)
        self.screen = Screen(TestSettings)
        self.settings = TestSettings
        self.tile_factory = TileFactory(self.settings)

TEST_GAME_CONTEXT = TestGameContext()


def showdoc(func):
    """
    decorator function showing a docstring
    """
    def do_show(self):
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT, (10,400), (400,50))
        tb = TextBox(frame, func.__doc__)
        tb.draw()
        pygame.display.update()
        func(self)
        time.sleep(DELAY)

    return do_show


TILE = 'test_data/test_tile.png'
TILE_SET = 'test_data/boxes.xpm'
TILE_SPECS = 'test_data/tiles.spec'

SAMPLE_MAP_FILE = 'test_data/sample.map'
HIGHSCORE_BACKUP = 'test_data/test_scores_backup.txt'

DELAY = 2.0
SHORT_DELAY = 0.05
VERY_SHORT_DELAY = 0.02
