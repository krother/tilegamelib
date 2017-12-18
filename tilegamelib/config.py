
import os

import pygame
import pygame.font
from pygame.rect import Rect

from .vector import Vector


pygame.font.init()


class BasicConfig:

    BASE_PATH = os.path.split(__file__)[0]
    DATA_PATH = os.path.join(BASE_PATH, '..', 'examples', 'data') + os.sep

    # tiles
    TILE_SET = DATA_PATH + 'tiles.xpm'
    TILE_SPECS = DATA_PATH + 'tiles.conf'

    # fonts
    FONT_FILE = os.path.join(DATA_PATH, 'LucidaSansDemiBold.ttf')
    DEMIBOLD_BIG = pygame.font.Font(FONT_FILE, 20)
    DEMIBOLD_SMALL = pygame.font.Font(FONT_FILE, 14)

    BLUE = (128, 128, 255, 0)

    DELAY = 0.01
    SHORT_DELAY = 0.05
    VERY_SHORT_DELAY = 0.02

    # screen
    RESOLUTION = Vector(800, 600)
    TILE_SIZE = Vector(32, 32)
    BACKGROUND_IMAGE = DATA_PATH + 'background.png'

    # colors
    WHITE = (255, 255, 255, 0)
    RED = (255, 128, 128, 0)
    GREEN = (128, 255, 128, 0)
    BLUE = (128, 128, 255, 0)
    GRAY = (128, 128, 128, 0)
    YELLOW = (255, 255, 128, 0)
    CYAN = (128, 255, 255, 0)
    MAGENTA = (255, 128, 255, 0)

    MAIN_MENU_RECT = Rect(0, 0, 750, 550)
    MAIN_MENU_IMAGE = DATA_PATH + 'title.png'
    MAIN_MENU_TEXTPOS = Rect(550, 380, 800, 550)
    # MENU_KEY_REPEAT = {274: 20, 115: 20}

    HIGHSCORES = False
    HIGHSCORE_RECT = Rect(200, 100, 800, 550)
    HIGHSCORE_IMAGE = DATA_PATH + 'background.png'
    HIGHSCORE_TEXT_POS = Vector(0, 0)

    GAME_OVER_IMAGE = DATA_PATH + 'frame_box.png'
    GAME_OVER_RECT = Rect(200, 150, 400, 100)
    GAME_OVER_OFFSET = Vector(120, 30)
    GAME_OVER_SHORT_OFFSET = Vector(50, 30)
    GAME_OVER_RECT = Rect(200, 150, 400, 100)
    GAME_OVER_COLOR = (255, 255, 255, 0)
    GAME_OVER_DELAY = 1000
    GAME_OVER_SOUND = {}

    # pause box
    PAUSE_BOX_RECT = Rect(200, 150, 400, 100)
    PAUSE_IMAGE = DATA_PATH + '/frame_box.png'
    PAUSE_TEXT = "Game Paused - press any key to continue"

    def read_config(filename):
        '''reads lines from config file into a dictionary.'''
        result = {}
        for line in open(filename):
            if '=' in line:
                name, value = line.split('=')
                result[name.strip()] = eval(value.strip())
        return result

config = BasicConfig()
