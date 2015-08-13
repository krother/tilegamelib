
import pygame.font
from pygame.rect import Rect
from vector import Vector
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE

# fonts
pygame.font.init()
#DEMIBOLD_BIG = pygame.font.Font('data/LucidaSansDemiBold.ttf', 20)
#DEMIBOLD_SMALL = pygame.font.Font('data/LucidaSansDemiBold.ttf', 14)

# colors
WHITE   = (255, 255, 255, 0)
RED     = (255, 128, 128, 0)
GREEN   = (128, 255, 128, 0)
BLUE    = (128, 128, 255, 0)
GRAY    = (128, 128, 128, 0)
YELLOW  = (255, 255, 128, 0)
CYAN    = (128, 255, 255, 0)
MAGENTA = (255, 128, 255, 0)


def read_settings(filename):
    '''reads lines from settings file into a dictionary.'''
    result = {}
    for line in open(filename):
        if '=' in line:
            name, value = line.split('=')
            result[name.strip()] = eval(value.strip())
    return result


