
import time

import pygame
import pytest

from tilegamelib.config import config
from tilegamelib.map_move import MapMove
from tilegamelib.move_group import MoveGroup
from tilegamelib.tiled_map import TiledMap
from tilegamelib.vector import DOWNLEFT, UP, Vector


@pytest.fixture
def tiled_map(game):
    return TiledMap(game)


class TestTiledMap:

    def test_fill_map(self, tiled_map):
        tiled_map.set_map(TEST_MAP)

    def test_caching(self, tiled_map):
        """Performance test"""
        bigmap = ["." * 50 for i in range(50)]
        tiled_map.set_map('\n'.join(bigmap))
        for i in range(10):
            tiled_map._cache_map()

    def test_win_size(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        assert tiled_map.win_size.x == 10
        assert tiled_map.win_size.y == 10

    def test_is_visible(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        assert tiled_map.is_on_screen((0, 0))
        assert tiled_map.is_on_screen((1, 1))
        assert not tiled_map.is_on_screen((11, 1))
        assert not tiled_map.is_on_screen((1, 11))
        assert not tiled_map.is_on_screen((-5, -1))

    def test_set_tile(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        tiled_map.set_tile((3, 3), 'x')
        assert tiled_map.at((3, 3)) == 'x'

    def test_is_on_map(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        assert not tiled_map.is_on_map((-1, -1))
        assert not tiled_map.is_on_map((5, 1))
        assert not tiled_map.is_on_map((1, 5))
        assert tiled_map.is_on_map((0, 0))
        assert tiled_map.is_on_map((1, 1))
        assert tiled_map.is_on_map((4, 4))

    def test_check_move(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        assert not tiled_map.check_move((-1, -1))
        assert tiled_map.check_move((1, 1))
        tiled_map.zoom_to((15, 15))
        assert not tiled_map.check_move((1, 1))
        assert tiled_map.check_move((-1, -1))

    def test_zoom_to(self, tiled_map):
        tiled_map.set_map(TEST_MAP)
        tiled_map.zoom_to(Vector(1, 1))
        assert tiled_map.map_pos.x == 1
        assert tiled_map.map_pos.y == 1

    def test_get_map(self, tiled_map):
        tiled_map.set_map("ab\ncd")
        s = tiled_map.get_map()
        assert "ab\ncd" == s

    def test_draw(self, tiled_map, sample_map):
        """Draws two 5x5 locations of a map with boxes."""
        tiled_map.set_map(sample_map)
        tiled_map.draw()
        pygame.display.update()
        time.sleep(config.DELAY)
        tiled_map.zoom_to(Vector(4, 4))
        tiled_map.draw()
        pygame.display.update()

    def test_move_map_tile(self, tiled_map, game, sample_map):
        """Moves two tiles smoothly."""
        tiled_map.set_map(sample_map)
        tiled_map.draw()
        moves = MoveGroup([
            MapMove(tiled_map, (3, 1), DOWNLEFT, 1,
                floor_tile='a', insert_tile='#'),
            MapMove(tiled_map, (3, 2), UP, 1,
                floor_tile='b', insert_tile='#')
        ])
        game.wait_for_move(moves, tiled_map.draw, 0.01)


TEST_MAP = """#...#
.aaa.
.p#b.
.aaa.
#...#"""

TEST_LINES = [".....", ".....", ".....", ".....", "....."]
