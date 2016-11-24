
import os
import pygame


BASE_PATH = os.path.split(__file__)[0]
DATA_PATH = BASE_PATH + '/../examples/data/'

pygame.font.init()
DEMIBOLD_BIG = pygame.font.Font(DATA_PATH + 'LucidaSansDemiBold.ttf', 20)

BLUE = (128, 128, 255, 0)
