#! /usr/bin/python

from tilegamelib import Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.vector import LEFT, UP, DOWN
from tilegamelib.basic_boxes import DictBox
from tilegamelib.draw_timer import draw_timer
from pygame import Rect
import random
import time
import pygame

MOVE_DELAY = 50
SHIP_SPEED = 4

LEVEL = """####################
....................
....................
....................
....................
....................
....................
....................
....................
....................
....................
####################"""


class SpaceMine:

    def __init__(self, level, tile_factory, pos):
        self.level = level
        tile = tile_factory.get('+')
        self.sprite = Sprite(level.tmap.frame, tile, pos)
        [self.sprite.add_move(LEFT) for x in range(10)]

    def draw(self):
        self.sprite.draw()


class SpaceshipLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.tmap.cache_map()
        self.mines = [self.create_mine() for x in range(4)]
        self.max_mines = 60
        self.max_add_mines = 4

    def at(self, pos):
        return self.tmap.at(pos)

    def create_mine(self):
        x = 21
        y = random.randint(1, self.tmap.size.y - 2)
        mine = SpaceMine(self, self.tmap.tile_factory, Vector(x, y))
        for i in range(x + 1):
            mine.sprite.add_move(LEFT)
        return mine

    def draw(self):
        for mine in self.mines:
            mine.sprite.move()

        self.tmap.draw()

        for mine in self.mines:
            mine.draw()
        self.mines = [m for m in self.mines if not mine.sprite.finished]
        if random.randint(1, 30) == 1:
            self.mines.append(self.create_mine())


class SpaceshipSprite:

    def __init__(self, frame, tile_factory, pos, level):
        self.frame = frame
        self.tile_factory = tile_factory
        self.level = level
        self.sprite = None
        self.create_sprite(pos)
        self.direction = DOWN
        self.crashed = False
        self.finished = False

    def is_moving(self):
        if not self.sprite.finished:
            return True

    def create_sprite(self, pos):
        tile = self.tile_factory.get('rot.rechts')
        self.sprite = Sprite(self.frame, tile, pos, SHIP_SPEED)

    def set_direction(self, direction):
        if direction in (UP, DOWN):
            self.direction = direction
            self.sprite.add_move(self.direction)
            newpos = self.sprite.pos + self.direction
            tile = self.level.at(newpos)
            if tile in ('#', '+'):
                self.crashed = True

    def draw(self):
        if self.is_moving():
            self.sprite.move()
        self.sprite.draw()

    @property
    def position(self):
        return self.sprite.pos

    def move_forward(self):
        pass


class SpaceRaceGame:

    def __init__(self, screen):
        self.screen = screen
        self.tile_factory = TileFactory('data/tiles.conf')

        self.level = None
        self.spaceship = None
        self.status_box = None
        self.events = None
        self.score = 0

        self.create_level()
        self.create_status_box()

        self.update_mode = self.update_ingame
        self.move_delay = MOVE_DELAY
        self.delay = MOVE_DELAY

    def create_level(self):
        frame = Frame(self.screen, Rect(10, 10, 640, 512))
        tmap = TiledMap(frame, self.tile_factory)
        self.level = SpaceshipLevel(LEVEL, tmap)
        self.spaceship = SpaceshipSprite(frame, self.tile_factory, Vector(1, 1), self.level)

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 50))
        self.status_box = DictBox(frame, {'score': 0})

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.spaceship.is_moving():
            pygame.display.update()
            time.sleep(1)
            self.events.exit_signalled()

    def update_ingame(self):
        self.delay -= 1
        if self.delay <= 0:
            self.delay = self.move_delay
            self.spaceship.move_forward()
        if self.spaceship.crashed:
            self.update_mode = self.update_finish_moves
            self.score = 0
        if self.spaceship.finished:
            self.update_mode = self.update_finish_moves
            self.score = 1000

    def draw(self):
        self.update_mode()
        self.level.draw()
        self.spaceship.draw()
        self.status_box.draw()
        pygame.display.update()
        #time.sleep(0.01)

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.spaceship.set_direction))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/snake.conf', SpaceRaceGame)
    game.run()

