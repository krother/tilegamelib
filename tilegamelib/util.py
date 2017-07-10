
import os
import pygame


BASE_PATH = os.path.split(__file__)[0]
DATA_PATH = os.path.join(BASE_PATH, '..', 'examples', 'data') + os.sep

pygame.font.init()
FONT_FILE = os.path.join(DATA_PATH, 'LucidaSansDemiBold.ttf')
DEMIBOLD_BIG = pygame.font.Font(FONT_FILE, 20)

BLUE = (128, 128, 255, 0)
