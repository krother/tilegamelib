
import pygame
import os
import pygame.font
from pygame.rect import Rect

from .vector import Vector

pygame.font.init()


class BasicConfig:

    BASE_PATH = os.path.split(__file__)[0]
    DATA_PATH = os.path.join(BASE_PATH, '..', 'examples', 'data') + os.sep

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
    WHITE   = (255, 255, 255, 0)
    RED     = (255, 128, 128, 0)
    GREEN   = (128, 255, 128, 0)
    BLUE    = (128, 128, 255, 0)
    GRAY    = (128, 128, 128, 0)
    YELLOW  = (255, 255, 128, 0)
    CYAN    = (128, 255, 255, 0)
    MAGENTA = (255, 128, 255, 0)

    def read_config(filename):
        '''reads lines from config file into a dictionary.'''
        result = {}
        for line in open(filename):
            if '=' in line:
                name, value = line.split('=')
                result[name.strip()] = eval(value.strip())
        return result

config = BasicConfig()
