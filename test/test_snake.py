
"""
import time

import pygame
from pygame.rect import Rect

from tilegamelib import Game, TiledMap
from tilegamelib.frame import Frame
from tilegamelib.vector import DOWN, LEFT, RIGHT, UP, Vector
from snake import SnakeController
from snake import SnakeGameState
from snake import SnakeLevel
from snake import SnakeSprite
from snake import TILE_SYNONYMS
"""


box = """########
#......#
#......#
#....a.#
#......#
#......#
########"""

empty_box = """########
#......#
#......#
#......#
#......#
#......#
########"""

twofruit_box = """########
#......#
#.b....#
#....a.#
#......#
#......#
########"""

"""
class _SnakeLevel_notest:

    def setUp(self):
        self.level = SnakeLevel(box)

    def test_get_set(self):
        self.assertEqual(str(self.level), box)
        self.level.set_level(empty_box)
        self.assertEqual(str(self.level), empty_box)

    def test_place_fruit(self):
        self.level.place_fruit(Vector(2, 2), 'b')
        self.assertEqual(str(self.level), twofruit_box)

    def test_place_random_fruit(self):
        self.level.place_random_fruit()

    def test_remove_fruit(self):
        self.level.remove_fruit(Vector(5, 3))
        self.assertEqual(str(self.level), empty_box)

    def test_get(self):
        self.assertEqual(self.level.get(Vector(5, 3)), 'a')
        self.assertEqual(self.level.get(Vector(4, 4)), '.')
        self.assertEqual(self.level.get(Vector(0, 0)), '#')

    def test_display(self):
        gf = GameFactory('data/settings.txt')
        frame = Frame(gf.screen, Rect(0, 0, 512, 256))
        gf.tile_factory.add_tile_synonyms(TILE_SYNONYMS)
        self.level.place_fruit(Vector(2, 2), 'b')
        tmap = TiledMap(frame, gf.tile_factory)
        tmap.fill_map(str(self.level))
        tmap.cache_map()
        tmap.draw()
        pygame.display.update()
        time.sleep(1)


class SnakeSpriteTests_notest:

    def setUp(self):
        self.gf = GameFactory('data/settings.txt')
        frame = Frame(self.gf.screen, Rect(0, 0, 512, 256))
        self.snake = SnakeSprite(frame, self.gf, Vector(5, 5))

    def run_snake(self):
        while self.snake.is_moving():
            self.gf.screen.clear()
            self.snake.update()
            self.snake.draw()
            pygame.display.update()
            time.sleep(0.03)

    def test_draw_snake(self):
        '''Display snake head'''
        self.snake.draw()
        pygame.display.update()
        time.sleep(0.5)

    def test_move_snake(self):
        '''Snake moves into four directions.'''
        for move in (UP, LEFT, DOWN, RIGHT):
            self.snake.add_move(move, [])
        self.run_snake()

    def test_add_tail(self):
        '''Snake moves with tail segment.'''
        self.snake.add_tail_segment()
        for move in (RIGHT, RIGHT, RIGHT, RIGHT):
            self.snake.add_move(move, [RIGHT])
        self.run_snake()

    def test_add_long_tail(self):
        '''Snake moves into four directions.'''
        self.snake.add_tail_segment()
        self.snake.add_move(RIGHT, [RIGHT])
        self.snake.add_tail_segment()
        self.snake.add_move(UP, [RIGHT, RIGHT])
        self.snake.add_move(UP, [UP, RIGHT])
        self.snake.add_tail_segment()
        self.snake.add_move(LEFT, [UP, UP, RIGHT])
        self.snake.add_move(LEFT, [LEFT, UP, UP])
        self.snake.add_move(LEFT, [LEFT, LEFT, UP])
        self.run_snake()


class _SnakeController_notest:

    def setUp(self):
        self.level = SnakeLevel(box)
        self.gf = GameFactory('data/settings.txt')
        self.frame = Frame(self.gf.screen, Rect(0, 0, 512, 256))
        self.gf.tile_factory.add_tile_synonyms(TILE_SYNONYMS)
        pos = Vector(5, 5)
        self.snake = SnakeSprite(self.frame, self.gf, pos)
        self.control = SnakeController(pos, RIGHT, self.level, self.snake)

    def show(self):
        tmap = TiledMap(self.frame, self.gf.tile_factory)
        tmap.fill_map(str(self.level))
        tmap.cache_map()
        while self.snake.is_moving():
            self.snake.update()
            tmap.draw()
            self.snake.draw()
            pygame.display.update()
            time.sleep(0.03)

    def test_move(self):
        self.assertEqual(self.control.pos, Vector(5, 5))
        self.control.up()
        self.assertEqual(self.control.pos, Vector(5, 4))
        self.control.left()
        self.assertEqual(self.control.pos, Vector(4, 4))
        self.control.right()
        self.assertEqual(self.control.pos, Vector(5, 4))
        self.control.down()
        self.assertEqual(self.control.pos, Vector(5, 5))

    def test_crash(self):
        self.control.right()
        self.control.up()
        self.assertFalse(self.control.crashed)
        self.control.right()
        self.assertTrue(self.control.crashed)

    def test_grow(self):
        self.control.grow()
        self.assertEqual(len(self.control.positions), 2)
        self.assertEqual(self.control.positions[1], Vector(5, 5))
        self.control.up()
        self.assertEqual(len(self.control.positions), 2)
        self.assertEqual(self.control.positions[1], Vector(5, 5))
        self.control.up()  # there is a fruit here
        self.assertEqual(len(self.control.positions), 3)
        self.assertEqual(self.control.positions[1], Vector(5, 4))
        self.assertEqual(self.control.positions[2], Vector(5, 5))
        self.control.up()
        self.assertEqual(len(self.control.positions), 3)
        self.assertEqual(self.control.positions[2], Vector(5, 4))
        self.control.left()
        self.assertEqual(self.control.positions[0], Vector(4, 2))
        self.assertEqual(self.control.positions[1], Vector(5, 2))
        self.assertEqual(self.control.positions[2], Vector(5, 3))
        self.show()
"""
