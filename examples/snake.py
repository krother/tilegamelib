#! /usr/bin/python

import random
import time

import pygame
from pygame import Rect

from tilegamelib import EventGenerator
from tilegamelib import ExitListener
from tilegamelib import FigureMoveListener
from tilegamelib import Frame
from tilegamelib import TiledMap
from tilegamelib import TileFactory
from tilegamelib.basic_boxes import DictBox
from tilegamelib.draw_timer import draw_timer
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP
from tilegamelib.vector import Vector

MOVE_DELAY = 15


LEVEL = """####################
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
#..................#
####################"""

MOVE_OK = 1
MOVE_CRASH = 2
HEAD_SPEED = 4

HEAD_TILES = {
    UP: 'b.pac_up',
    DOWN: 'b.pac_down',
    LEFT: 'b.pac_left',
    RIGHT: 'b.pac_right'
}

EASY = False


class SnakeLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.tmap.cache_map()

    def at(self, pos):
        return self.tmap.at(pos)

    def place_fruit(self, pos, fruit):
        self.tmap.set_tile(pos, fruit)
        self.tmap.cache_map()

    def remove_fruit(self, pos):
        tile = self.at(pos)
        if tile != '.':
            self.tmap.set_tile(pos, '.')
            self.tmap.cache_map()

    def place_random_fruit(self):
        x = random.randint(1, self.tmap.size.x - 2)
        y = random.randint(1, self.tmap.size.y - 2)
        fruit = random.randint(0, 5)
        self.place_fruit(Vector(x, y), 'abcdef'[fruit])

    def draw(self):
        self.tmap.draw()


class SnakeSprite:

    def __init__(self, frame, tile_factory, pos, level):
        self.frame = frame
        self.tile_factory = tile_factory
        self.level = level
        self.head = None
        self.tail = []
        self.tail_waiting = []
        self.create_head(pos)
        self.direction = RIGHT
        self.past_directions = []
        self.crashed = False
        self.eaten = ''

    @property
    def length(self):
        return 1 + len(self.tail) + len(self.tail_waiting)

    @property
    def sprites(self):
        return [self.head] + self.tail

    def is_moving(self):
        if not self.head.finished:
            return True

    def create_head(self, pos):
        tile = self.tile_factory.get('b.pac_right')
        self.head = Sprite(self.frame, tile, pos, HEAD_SPEED)

    def set_direction(self, direction):
        # prevent reverse move
        if self.tail and direction == self.past_directions[0] * -1:
            return
        self.direction = direction
        headtile = HEAD_TILES[direction]
        self.head.tile = self.tile_factory.get(headtile)
        if EASY:
            self.move_forward()

    def draw(self):
        for s in self.sprites:
            s.draw()

    def move(self):
        if self.is_moving():
            for s in self.sprites:
                s.move()

    @property
    def positions(self):
        return [self.head.pos] + [seg.pos for seg in self.tail]

    def grow(self):
        tile = self.tile_factory.get('b.tail')
        self.tail_waiting.append(Sprite(self.frame, tile, self.positions[-1], HEAD_SPEED))
        if not self.past_directions:
            self.past_directions.append(self.direction)
        else:
            self.past_directions.append(self.past_directions[-1])

    def move_forward(self):
        newpos = self.head.pos + self.direction
        tile = self.level.at(newpos)
        if newpos in self.positions or tile == '#':
            self.crashed = True
        else:
            self.head.add_move(self.direction)
            if self.tail_waiting:
                self.tail.append(self.tail_waiting.pop())
            for sprite, direction in zip(self.tail, self.past_directions):
                sprite.add_move(direction)
            if tile != '.':
                self.grow()
                self.eaten = tile
            if len(self.tail) > 0:
                self.past_directions = [self.direction] + self.past_directions[:-1]


class SnakeGame:

    def __init__(self, screen):
        self.screen = screen
        self.tile_factory = TileFactory('data/tiles.conf')

        self.level = None
        self.snake = None
        self.status_box = None
        self.events = None
        self.score = 0

        self.create_level()
        self.create_snake()
        self.create_status_box()

        self.update_mode = self.update_ingame
        self.move_delay = MOVE_DELAY
        self.delay = MOVE_DELAY

    def create_snake(self):
        start_pos = Vector(5, 5)
        frame = Frame(self.screen, Rect(10, 10, 640, 512))
        self.snake = SnakeSprite(frame, self.tile_factory,
                                 start_pos, self.level)
        self.snake.set_direction(RIGHT)

    def create_level(self):
        frame = Frame(self.screen, Rect(10, 10, 640, 512))
        tmap = TiledMap(frame, self.tile_factory)
        self.level = SnakeLevel(LEVEL, tmap)
        self.level.place_random_fruit()

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 200))
        self.status_box = DictBox(frame, {'score': 0})

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.snake.is_moving():
            pygame.display.update()
            time.sleep(1)
            self.events.exit_signalled()

    def update_ingame(self):
        self.delay -= 1
        if self.delay <= 0:
            self.delay = self.move_delay
            if not EASY:
                self.snake.move_forward()
        if self.snake.eaten and not self.snake.is_moving():
            self.level.remove_fruit(self.snake.head.pos)
            self.level.place_random_fruit()
            self.status_box.data['score'] += 100
            self.snake.eaten = None
        if self.snake.crashed:
            self.update_mode = self.update_finish_moves
            self.score = self.status_box.data['score']

    def update(self):
        self.update_mode()
        self.snake.move()

    def draw(self):
        self.update()
        self.level.draw()
        self.snake.draw()
        self.status_box.draw()
        pygame.display.update()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.snake.set_direction))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/snake.conf', SnakeGame)
    game.run()
