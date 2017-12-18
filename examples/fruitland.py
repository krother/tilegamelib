
import time

import pygame
from pygame import Rect

from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib.config import config

if __name__ == '__main__':
    fruitmap = """################
#..aa..bb..cc..#
#..aa..bb..cc..#
#cc..dd..ee..ff#
#cc..dd..ee..ff#
#..bb..cc..ee..#
#..bb..cc..ee..#
#ee..ff..gg..hh#
#ee..ff..gg..hh#
#..aa..bb..cc..#
#..aa..bb..cc..#
#cc..dd..ee..ff#
#cc..dd..ee..ff#
################"""

    config.RESOLUTION = (320, 256)
    screen = Screen()
    frame = Frame(screen, Rect(0, 0, 320, 256))
    tile_factory = TileFactory()
    tm = TiledMap(frame, tile_factory)

    tm.set_map(fruitmap)
    tm.draw()
    pygame.display.update()
    for i in list(range(0, 224, 2)) + list(range(224, 0, -4)):
        tm.offset = (i, i)
        screen.clear()
        tm.draw()
        pygame.display.update()
        time.sleep(0.025)
    time.sleep(1.0)
    pygame.quit()
