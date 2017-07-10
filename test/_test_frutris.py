
from random import randint
import time

import pygame
from pygame import Rect

from frutris import FrutrisBox
from tilegamelib import Frame
from tilegamelib import Screen
from tilegamelib import Sprite
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib import Vector
from tilegamelib.move import wait_for_move

if __name__ == '__main__':
    LEVEL = """#......#
#......#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""


    screen = Screen(Vector(800,550), 'data/background.png')
    frame = Frame(screen, Rect(64, 64, 320, 320))
    tile_factory = TileFactory('data/tiles.conf')
    frutris = FrutrisBox(frame, tile_factory, LEVEL)

    screen.clear()
    frutris.draw()
    pygame.display.update()
    time.sleep(0.5)
    frutris.level.insert(Vector(4, 5), 'd')
    frutris.level.draw()
    pygame.display.update()
    time.sleep(0.5)
    for i in range(3):
        frutris.level.remove_fruit()
        wait_for_move(frutris, screen, frutris.draw)
        frutris.level.drop_bricks()
        wait_for_move(frutris, screen, frutris.draw)
    # test diamond
    frutris.insert_diamond(2)
    for i in range(10):
        frutris.moving.drop()
        wait_for_move(frutris, screen, frutris.draw)
    # test fruit pair
    frutris.insert_fruit_pair('a', 'b')
    frutris.moving.drop()
    wait_for_move(frutris, screen, frutris.draw)
    frutris.moving.drop()
    wait_for_move(frutris, screen, frutris.draw)
    for i in range(4):
        frutris.moving.left_shift()
        wait_for_move(frutris, screen, frutris.draw)
    for i in range(4):
        frutris.moving.right_shift()
        wait_for_move(frutris, screen, frutris.draw)
    for i in range(4):
        frutris.moving.rotate()
        wait_for_move(frutris, screen, frutris.draw)
    for i in range(6):
        frutris.moving.drop()
        wait_for_move(frutris, screen, frutris.draw)
    
    time.sleep(2)
