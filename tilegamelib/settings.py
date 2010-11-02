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
from numpy import array

class BasicSettings:
    """
    Abstract class for keeping game parameters.
    """
    # screen setup
    ORIGIN = array([0,0])
    RESOLUTION = array([800, 600])
    TILE_SIZE = array([32, 32])

    # main delay in milliseconds
    DEFAULT_GAME_DELAY = 20

    # keys             
    EXIT_KEY = 27 # escape
    SPACE_KEY = 32 # space bar
    ENTER_KEY = 13 # enter
    BACKSPACE_KEY = 8 # <- delete

    # key delays
    KEY_REPEAT = {274:20, 115:20}
    DEFAULT_KEY_REPEAT = 40

    # direction vectors for various moves
    UP    = array([ 0,-1])
    DOWN  = array([ 0, 1])
    LEFT  = array([-1, 0])
    RIGHT = array([ 1, 0])
    UPLEFT    = array([-1,-1])
    DOWNLEFT  = array([-1, 1])
    UPRIGHT   = array([ 1,-1])
    DOWNRIGHT = array([ 1, 1])

    # colors
    WHITE   = (255,255,255,0)
    RED     = (255,128,128,0)
    GREEN   = (128,255,128,0)
    BLUE    = (128,128,255,0)
    GRAY    = (128,128,128,0)
    YELLOW  = (255,255,128,0)
    CYAN    = (128,255,255,0)
    MAGENTA = (255,128,255,0)

    BACKGROUND_IMAGE = None

    # important for testing!
    KEY_EVENT_QUEUE = None


class DialogSettings(BasicSettings):
    """
    Parameters for dialog boxes
    """    
    TITLE_IMAGE = None
    BOX_IMAGE = None
    TITLE_POS = array([0,0])
    TITLE_SIZE = array([750,550])

    # movement keymaps
    MENU_MOVES = { 273:'up', 274:'down', 
                   BasicSettings.ENTER_KEY:'select',
                   BasicSettings.SPACE_KEY:'select',
                   BasicSettings.EXIT_KEY:'quit'} 
    PLR1_MOVES = { 119:'up', 115:'down', 100:'right', 97:'left'} # w.s.d.a.
    PLR2_MOVES = { 273:'up', 274:'down', 275:'right', 276:'left', BasicSettings.EXIT_KEY:'quit'} # cursor keys

    # fonts
    pygame.font.init()
    DEMIBOLD_BIG = None
    DEMIBOLD_SMALL = None

    # menu box
    MAIN_MENU_POS = array([550,380])
    MAIN_MENU_SIZE = array([800,550])
    MAIN_MENU = [
        ('One player game','one player game'),
        ('Two player game','two player game'),
        ('Quit','quit')
        ]

    # game over box
    GAME_OVER_POS = array([200,150])
    GAME_OVER_SIZE = array([400,100])
    GAME_OVER_DELAY = 2500
    GAME_OVER_OFFSET = array([120,30])
    GAME_OVER_SHORT_OFFSET = array([50,30])
    GAME_OVER_SOUND = {}

    # box appearing while paused
    PAUSE_BOX_POS = array([200,150])
    PAUSE_BOX_SIZE = array([400,100])
    PAUSE_KEY = 112

    # high score window
    HIGHSCORE_FILE = None
    HIGHSCORE_POS = array([0,0])
    HIGHSCORE_SIZE = array([800,550])
    HIGHSCORE_TEXT_POS = array([0,0])
    HIGHSCORE_IMAGE = None
    HIGHSCORE_LENGTH = 10

    # tiles
    TILE_SETS = []
    TILE_SYNONYMS = []
