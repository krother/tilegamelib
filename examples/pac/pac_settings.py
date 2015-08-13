
import pygame
import pygame.font
import numpy as np
from tilegamelib.settings import BasicSettings
from tilegamelib.vector import Vector

class PacSettings(BasicSettings):
    """
    Parameters for Frutris
    """
    RESOLUTION = Vector(800, 550)
    BACKGROUND_IMAGE = 'data/background.png'
    TITLE_IMAGE = 'data/title.png'
    BOX_IMAGE = 'data/frame_box.png'

    # fonts
    pygame.font.init()
    DEMIBOLD_BIG = pygame.font.Font('data/LucidaSansDemiBold.ttf',20)
    DEMIBOLD_SMALL = pygame.font.Font('data/LucidaSansDemiBold.ttf',14)

    # high score window
    HIGHSCORE_FILE = 'pac_scores.txt'
    HIGHSCORE_IMAGE = 'data/background.png'

    DEFAULT_GAME_DELAY = 30
    
    KEY_REPEAT = {}
    MENU_KEY_REPEAT = {}
    GAME_KEY_REPEAT = { 273:1, 274:1, 275:1, 276:1}

    # tiles
    TILE_SETS = [('data/bg.xpm','data/bg.spec'),
                 ('data/fruit.xpm','data/fruit.spec')
                 ]

    TILE_SYNONYMS = [('#','b.wall'),('.','b.empty'),
                     ('a','b.dot'),('b','f.orange'),
                     ('c','f.melon'),('d','f.pineapple'),
                     ('e','f.winogrona'),('f','f.cherry'),
                     ('g','f.paprika'),
                     ('h','f.diamond'),
                     ('p','b.pac_right'),
                     ]
    FRUIT_NAMES = dict(TILE_SYNONYMS)

    FRUITS = ['f.banana','f.orange','f.melon','f.pineapple',\
              'f.winogrona','f.diamond','f.cherry','f.paprika']

