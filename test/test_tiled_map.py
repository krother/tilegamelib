
from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT, UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT
from tilegamelib.frame import Frame
from tilegamelib.move import Move
from tilegamelib.tiled_map import TiledMap, MoveableTiledMap
from test_settings import DELAY, SHORT_DELAY, SAMPLE_MAP_FILE, \
    TEST_GAME_CONTEXT, showdoc
from unittest import TestCase, main
from pygame import Rect
import pygame
import time


class TiledMapTests(TestCase):

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90,50, 128,128))
        self.tm = TiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

    def test_fill_map(self):
        self.tm.fill_map(TEST_MAP)
        
    def test_parse_map(self):
        self.tm.parse_map(TEST_LINES)

    def test_caching(self):
        bigmap = ["."*50 for i in range(50)]
        self.tm.parse_map(bigmap)
        for i in range(10):
            self.tm.cache_map()

    def test_win_size(self):
        self.tm.fill_map(TEST_MAP)
        self.assertEqual(self.tm.win_size.x,4)
        self.assertEqual(self.tm.win_size.y,4)

    def test_is_visible(self):
        self.tm.fill_map(TEST_MAP)
        self.assertTrue(self.tm.is_visible(Vector(0,0)))
        self.assertTrue(self.tm.is_visible(Vector(1,1)))
        self.assertFalse(self.tm.is_visible(Vector(5,1)))
        self.assertFalse(self.tm.is_visible(Vector(1,5)))
        self.assertFalse(self.tm.is_visible(Vector(-5,-1)))

    def test_check_position(self):
        self.tm.fill_map(TEST_MAP)
        self.assertFalse(self.tm.check_position(Vector(-1,-1)))
        self.assertFalse(self.tm.check_position(Vector(5,1)))
        self.assertFalse(self.tm.check_position(Vector(1,5)))
        self.assertTrue(self.tm.check_position(Vector(0,0)))
        self.assertTrue(self.tm.check_position(Vector(1,1)))
        self.assertTrue(self.tm.check_position(Vector(4,4)))

    def test_check_move(self):
        self.tm.fill_map(TEST_MAP)
        self.assertFalse(self.tm.check_move(Vector(-1,-1)))
        self.assertTrue(self.tm.check_move(Vector(1,1)))
        self.tm.zoom_to(Vector(1,1))
        self.assertFalse(self.tm.check_move(Vector(1,1)))
        self.assertTrue(self.tm.check_move(Vector(-1,-1)))

    def test_zoom_to(self):
        self.tm.fill_map(TEST_MAP)
        self.tm.zoom_to(Vector(1, 1))
        self.assertEqual(self.tm.map_pos.x,1)
        self.assertEqual(self.tm.map_pos.y,1)

    def test_load_map(self):
        self.tm.load_map(SAMPLE_MAP_FILE)
        self.assertEqual(len(self.tm.map),10)
        self.assertEqual(len(self.tm.map[0]),10)

    @showdoc
    def test_draw(self):
        """Draws two 5x5 locations of a map with boxes."""
        self.tm.load_map(SAMPLE_MAP_FILE)
        self.tm.draw()
        pygame.display.update()
        time.sleep(DELAY)
        self.tm.zoom_to(Vector(4,4))
        self.tm.draw()
        pygame.display.update()
        

class MoveableTiledMapTests(TestCase):

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90,50, 160,160))
        self.tm = MoveableTiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

    def move_tiles(self):
        while self.tm.is_map_moving():
            self.tm.update()
            self.tm.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

    @showdoc
    def test_move_map_tile(self):
        """Moves two tiles right and up, then moves one tile back."""
        self.tm.fill_map(TEST_MAP)
        self.tm.move_tile(Move(Vector(3,1), DOWNLEFT, 3, 2))
        self.tm.move_tile(Move(Vector(1,2), UP, 1, 1))
        self.move_tiles()
        # move one piece back
        self.tm.move_tile(Move(Vector(0,0), DOWN, 1, 4))
        self.tm.move_tile(Move(Vector(0,4), UPRIGHT, 3, 2))
        self.move_tiles()

    @showdoc
    def test_queued_moves(self):
        """Two 2+1 moves across the map shown."""
        self.tm.fill_map(TEST_MAP)
        self.tm.add_queued_moveset(
                [Move(Vector(0,0), DOWN, 3, 2),
                 Move(Vector(2,1), UPLEFT, 1, 4)])
        self.tm.add_queued_moveset([Move(Vector(3,3), LEFT, 2, 1)])
        self.move_tiles()



TEST_MAP = """g...g
.rrr.
.pgb.
.rrr.
g...g"""

TEST_LINES = [".....",".....",".....",".....","....."]

if __name__ == "__main__":
    main()
