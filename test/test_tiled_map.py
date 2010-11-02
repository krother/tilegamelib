#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

from tilegamelib.screen import Frame
from tilegamelib.tiled_map import TiledMap, MoveableTiledMap, Move
from test_settings import DELAY, SHORT_DELAY, SAMPLE_MAP_FILE, \
    TEST_GAME_CONTEXT, showdoc
from unittest import TestCase, main
import numpy as np
import pygame
import time


class TiledMapTests(TestCase):

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT, (90,50), (128,128))
        self.tm = TiledMap(TEST_GAME_CONTEXT, frame)

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
        self.assertEqual(self.tm.win_size[0],4)
        self.assertEqual(self.tm.win_size[1],4)

    def test_is_visible(self):
        self.tm.fill_map(TEST_MAP)
        self.assertTrue(self.tm.is_visible(np.array([0,0])))
        self.assertTrue(self.tm.is_visible(np.array([1,1])))
        self.assertFalse(self.tm.is_visible(np.array([5,1])))
        self.assertFalse(self.tm.is_visible(np.array([1,5])))
        self.assertFalse(self.tm.is_visible(np.array([-5,-1])))

    def test_check_position(self):
        self.tm.fill_map(TEST_MAP)
        self.assertFalse(self.tm.check_position(np.array([-1,-1])))
        self.assertFalse(self.tm.check_position(np.array([5,1])))
        self.assertFalse(self.tm.check_position(np.array([1,5])))
        self.assertTrue(self.tm.check_position(np.array([0,0])))
        self.assertTrue(self.tm.check_position(np.array([1,1])))
        self.assertTrue(self.tm.check_position(np.array([4,4])))

    def test_check_move(self):
        self.tm.fill_map(TEST_MAP)
        self.assertFalse(self.tm.check_move(np.array([-1,-1])))
        self.assertTrue(self.tm.check_move(np.array([1,1])))
        self.tm.zoom_to(np.array([1,1]))
        self.assertFalse(self.tm.check_move(np.array([1,1])))
        self.assertTrue(self.tm.check_move(np.array([-1,-1])))

    def test_zoom_to(self):
        self.tm.fill_map(TEST_MAP)
        self.tm.zoom_to(np.array([1,1]))
        self.assertEqual(self.tm.map_pos[0],1)
        self.assertEqual(self.tm.map_pos[1],1)

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
        self.tm.zoom_to(np.array([4,4]))
        self.tm.draw()
        pygame.display.update()
        

class MoveableTiledMapTests(TestCase):

    def setUp(self):
        frame = Frame(TEST_GAME_CONTEXT, (90,50), (128,128))
        self.tm = MoveableTiledMap(TEST_GAME_CONTEXT, frame)

    def move_tiles(self):
        while self.tm.are_tiles_moving():
            self.tm.update()
            self.tm.draw()
            pygame.display.update()
            time.sleep(SHORT_DELAY)

    @showdoc
    def test_move_map_tile(self):
        """Moves two tiles right and up, then moves one tile back."""
        self.tm.fill_map(TEST_MAP)
        self.tm.move_tile(Move(np.array([2,2]), np.array([1,0]), 4, 2))
        self.tm.move_tile(Move(np.array([1,2]), np.array([0,-1]), 1, 1))
        self.move_tiles()
        # move piece back
        self.tm.move_tile(Move(np.array([4,2]), np.array([-1,0]), 2, 2))
        self.move_tiles()


TEST_MAP = """g...g
.rrr.
.bgb.
.rrr.
g...g"""

TEST_LINES = [".....",".....",".....",".....","....."]

if __name__ == "__main__":
    main()
