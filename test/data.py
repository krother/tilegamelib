#!/usr/bin/env python

from tilegamelib.vector import Vector
from pygame.rect import Rect
import pygame
import os

BASE_PATH = os.path.split(__file__)[0]
TEST_DATA_PATH = BASE_PATH + '/test_data/'
DATA_PATH = BASE_PATH + '/../examples/data/'

KEY_EVENT_QUEUE = [27]
SAMPLE_MAP_FILE = TEST_DATA_PATH + 'sample.map'

DELAY = 0.1
SHORT_DELAY = 0.05
VERY_SHORT_DELAY = 0.02

RESOLUTION = Vector(800, 600)
TILE_SIZE = Vector(32, 32)
BACKGROUND_IMAGE = DATA_PATH + 'background.png'

TILE = TEST_DATA_PATH + 'test_tile.png'
TILE_SET = TEST_DATA_PATH + 'tiles.xpm'
TILE_SPECS = DATA_PATH + 'tiles.conf'

pygame.font.init()
DEMIBOLD_BIG = pygame.font.Font(TEST_DATA_PATH + 'LucidaSansDemiBold.ttf', 20)
DEMIBOLD_SMALL = pygame.font.Font(TEST_DATA_PATH + 'LucidaSansDemiBold.ttf', 14)

# colors
WHITE = (255, 255, 255)

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
