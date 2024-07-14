
import time

from tilegamelib.games.frutris.frutris import FrutrisBox
from tilegamelib import Vector
from tilegamelib.config import config
from tilegamelib.vector import LEFT, RIGHT


def wait(box):
    while not box.moving_blocks.finished:
        box.moving_blocks.move()
        box.draw()
        #pygame.display.update()
        time.sleep(config.SHORT_DELAY)


def test_frutris(game):
    LEVEL = """#......#
#......#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

    frutris = FrutrisBox(game, LEVEL)

    # draw screen
    game.screen.clear()
    frutris.draw()
    pygame.display.update()
    time.sleep(0.5)

    # insert fruit
    frutris.level.insert(Vector(4, 5), 'd')
    frutris.level.draw()
    pygame.display.update()
    time.sleep(0.5)

    # remove fruits
    for i in range(3):
        frutris.remove_blocks()
        # wait_for_move(frutris, screen, frutris.draw)
        frutris.level.get_dropped_bricks()
        # wait_for_move(frutris, screen, frutris.draw)

    # test diamond
    frutris.insert_diamond(2)
    for i in range(10):
        wait(frutris)
        frutris.moving_blocks.drop()

    # test fruit pair
    frutris.insert_fruit_pair('a', 'b')

    # drop stuff
    frutris.moving_blocks.drop()
    wait(frutris)
    frutris.moving_blocks.drop()
    wait(frutris)

    # move stuff
    for _ in range(4):
        frutris.moving_blocks.shift(LEFT)
        wait(frutris)
    for i in range(4):
        frutris.moving_blocks.shift(RIGHT)
        wait(frutris)
    for i in range(4):
        frutris.moving_blocks.rotate()
        wait(frutris)
    for i in range(6):
        frutris.moving_blocks.drop()
        wait(frutris)

    time.sleep(2)
