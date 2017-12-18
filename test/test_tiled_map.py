
import time

import pygame
from pygame import Rect

from test.conftest import SAMPLE_MAP_FILE
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.map_move import MapMove
from tilegamelib.move import wait_for_move
from tilegamelib.move_group import MoveGroup
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import DOWNLEFT
from tilegamelib.vector import UP
from tilegamelib.vector import Vector
from util import showdoc
from util import TEST_GAME_CONTEXT


class TiledMapTests:

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90, 50, 128, 128))
        self.tm = TiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

    def test_fill_map(self):
        self.tm.set_map(TEST_MAP)

    def test_caching(self):
        bigmap = ["." * 50 for i in range(50)]
        self.tm.set_map('\n'.join(bigmap))
        for i in range(10):
            self.tm.cache_map()

    def test_win_size(self):
        self.tm.set_map(TEST_MAP)
        self.assertEqual(self.tm.win_size.x, 4)
        self.assertEqual(self.tm.win_size.y, 4)

    def test_is_visible(self):
        self.tm.set_map(TEST_MAP)
        self.assertTrue(self.tm.is_visible(Vector(0, 0)))
        self.assertTrue(self.tm.is_visible(Vector(1, 1)))
        self.assertFalse(self.tm.is_visible(Vector(5, 1)))
        self.assertFalse(self.tm.is_visible(Vector(1, 5)))
        self.assertFalse(self.tm.is_visible(Vector(-5, -1)))

    def test_check_position(self):
        self.tm.set_map(TEST_MAP)
        self.assertFalse(self.tm.check_position(Vector(-1, -1)))
        self.assertFalse(self.tm.check_position(Vector(5, 1)))
        self.assertFalse(self.tm.check_position(Vector(1, 5)))
        self.assertTrue(self.tm.check_position(Vector(0, 0)))
        self.assertTrue(self.tm.check_position(Vector(1, 1)))
        self.assertTrue(self.tm.check_position(Vector(4, 4)))

    def test_check_move(self):
        self.tm.set_map(TEST_MAP)
        self.assertFalse(self.tm.check_move(Vector(-1, -1)))
        self.assertTrue(self.tm.check_move(Vector(1, 1)))
        self.tm.zoom_to(Vector(1, 1))
        self.assertFalse(self.tm.check_move(Vector(1, 1)))
        self.assertTrue(self.tm.check_move(Vector(-1, -1)))

    def test_zoom_to(self):
        self.tm.set_map(TEST_MAP)
        self.tm.zoom_to(Vector(1, 1))
        self.assertEqual(self.tm.map_pos.x, 1)
        self.assertEqual(self.tm.map_pos.y, 1)

    @showdoc
    def test_draw(self):
        """Draws two 5x5 locations of a map with boxes."""
        self.tm.set_map(open(SAMPLE_MAP_FILE).read())
        self.tm.draw()
        pygame.display.update()
        time.sleep(config.DELAY)
        self.tm.zoom_to(Vector(4, 4))
        self.tm.draw()
        pygame.display.update()

    @showdoc
    def test_move_map_tile(self):
        """Moves two tiles right and up, then moves one tile back."""
        self.tm.set_map(open(SAMPLE_MAP_FILE).read())
        self.tm.draw()
        moves = MoveGroup()
        moves.add(MapMove(self.tm, Vector(3, 1), DOWNLEFT, 1,
            floor_tile='.', insert_tile='#'))
        moves.add(MapMove(self.tm, Vector(3, 2), UP, 1,
            floor_tile='.', insert_tile='#'))
        wait_for_move(moves, TEST_GAME_CONTEXT.screen, self.tm.draw, 0.01)


#     @showdoc
#     def test_queued_moves(self):
#         """Two 2+1 moves across the map shown."""
#         self.tm.set_map(TEST_MAP)
#         self.tm.add_queued_moveset(
#                 [Move(Vector(0,0), DOWN, 3, 2),
#                  Move(Vector(2,1), UPLEFT, 1, 4)])
#         self.tm.add_queued_moveset([Move(Vector(3,3), LEFT, 2, 1)])
#         self.move_tiles()


TEST_MAP = """#...#
.aaa.
.p#b.
.aaa.
#...#"""

TEST_LINES = [".....", ".....", ".....", ".....", "....."]
