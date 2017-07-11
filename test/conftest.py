#!/usr/bin/env python

import os

import pygame
from pygame.rect import Rect

from tilegamelib.vector import Vector
from tilegamelib.config import config

KEY_EVENT_QUEUE = [27]
TEST_DATA_PATH = config.BASE_PATH + '/../test/test_data/'
SAMPLE_MAP_FILE = TEST_DATA_PATH + 'sample.map'

TILE = TEST_DATA_PATH + 'test_tile.png'

# title screen
TITLE_IMAGE = TEST_DATA_PATH + 'test_tile.png'
TITLE_RECT = Rect(0, 0, 750, 550)
MENU_KEY_REPEAT = {274: 20, 115: 20}
MENU_RECT = Rect(550, 380, 800, 550)

# game over box
GAME_OVER_IMAGE = TEST_DATA_PATH + 'test_tile.png'
GAME_OVER_RECT = Rect(200, 150, 400, 100)
GAME_OVER_OFFSET = Vector(120, 30)
GAME_OVER_SHORT_OFFSET = Vector(50, 30)
GAME_OVER_RECT = Rect(200, 150, 400, 100)
GAME_OVER_COLOR = (255, 255, 255, 0)
GAME_OVER_DELAY = 1000
GAME_OVER_SOUND = {}

# pause box
PAUSE_IMAGE = TEST_DATA_PATH + 'test_tile.png'
PAUSE_BOX_RECT = Rect(200, 150, 400, 100)

# high score window
HIGHSCORE_RECT = Rect(200, 100, 800,550)
HIGHSCORE_IMAGE = TEST_DATA_PATH + 'test_tile.png'
HIGHSCORE_TEXT_POS = Vector(0, 0)
HIGHSCORE_FILE = TEST_DATA_PATH + 'test_scores.txt'
