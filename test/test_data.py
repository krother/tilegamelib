#!/usr/bin/env python

#from tilegamelib.game_factory import GameFactory
#from tilegamelib.frame import Frame
from tilegamelib.vector import Vector
from pygame.rect import Rect
import pygame
import time


KEY_EVENT_QUEUE = [27]
SAMPLE_MAP_FILE = 'test_data/sample.map'

DELAY = 0.1
SHORT_DELAY = 0.05
VERY_SHORT_DELAY = 0.02

RESOLUTION = Vector(800, 600)
BACKGROUND_IMAGE = 'test_data/background.png'

#GAME_FACTORY = GameFactory('test_data/settings.txt')
TILE = 'test_data/test_tile.png'
TILE_SET = 'test_data/tiles.xpm'
TILE_SPECS = 'test_data/tiles.spec'

DEMIBOLD_BIG = pygame.font.Font('test_data/LucidaSansDemiBold.ttf', 20)
DEMIBOLD_SMALL = pygame.font.Font('test_data/LucidaSansDemiBold.ttf', 14)

def showdoc(func):
    """
    decorator function showing a docstring
    """
    def wrap_test(self):
        """Clear screen, show docstring, run test."""
        GAME_FACTORY.screen.clear()
        frame = Frame(GAME_FACTORY.screen, Rect(10, 400, 400, 50))
        frame.clear()
        frame.print_text(func.__doc__, Vector(0, 0))
        pygame.display.update()
        func(self)
        time.sleep(DELAY)

    return wrap_test

def next_frame():
    pygame.display.update()
    time.sleep(DELAY)

def graphictest(func):
    """
    decorator function updating display and waiting
    """
    def wrap_test(self):
        func(self)
        next_frame()

    return wrap_test

#for key, value in GAME_FACTORY.data.items():
#    eval('%s = %s'%(key, value))

