
import pygame
import pygame.font
from tilegamelib.settings import DialogSettings
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
    BOX_IMAGE = 'test_data/test_tile.png'

    # high score window
    HIGHSCORE_FILE = 'test_data/test_scores.txt'
    HIGHSCORE_IMAGE = 'test_data/test_tile.png'

    GAME_OVER_DELAY = 1000



SAMPLE_MAP_FILE = 'test_data/sample.map'
HIGHSCORE_BACKUP = 'test_data/test_scores_backup.txt'


