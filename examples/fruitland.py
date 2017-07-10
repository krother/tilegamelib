
from tilegamelib import Screen, Frame, TileFactory, TiledMap, Vector
from tilegamelib.util import DATA_PATH
from pygame import Rect
import pygame
import time



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

    screen = Screen(Vector(256, 256), DATA_PATH + 'background.png')
    frame = Frame(screen, Rect(0, 0, 256, 256))
    tile_factory = TileFactory(DATA_PATH + 'tiles.conf')
    tm = TiledMap(frame, tile_factory)

    tm.set_map(fruitmap)
    tm.draw()
    pygame.display.update()
    for i in list(range(0, 224, 2)) + list(range(224, 0, -4)):
        tm.offset = Vector(i, i)
        screen.clear()
        tm.draw()
        pygame.display.update()
        time.sleep(0.05)
