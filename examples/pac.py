#! /usr/bin/python

from tilegamelib import Screen, Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener
from tilegamelib.sprites import Sprite
from tilegamelib.basic_boxes import DictBox
from tilegamelib.bar_display import BarDisplay
from tilegamelib.events import EventGenerator
from tilegamelib.sprites import Sprite
from tilegamelib.game import Game
from tilegamelib.draw_timer import draw_timer
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from pygame import Rect
import random
import pygame
import time

ONE_PLAYER_START_DELAY = 10


LEVEL = """####################
#.****************e#
#*#*#####**#####*#*#
#*#******cc******#*#
#*#*#####**#####*#*#
#******************#
#*##*###*f**###*##*#
#*##*###*f**###*##*#
#******************#
#*#*###**##**##*##*#
#e****************e#
####################"""

PAC_START = Vector(1, 1)
GHOST_POSITIONS = [Vector(18, 1),
                   Vector(18, 10),
                   Vector(1, 10)]

PAC_TILES = {
    UP: 'b.pac_up',
    DOWN: 'b.pac_down',
    LEFT: 'b.pac_left',
    RIGHT: 'b.pac_right'
}

GHOST_TILE = 'b.ghost'


class PacLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.tmap.cache_map()
        self.dots_left = data.count("*")

    def at(self, pos):
        return self.tmap.at(pos)

    def remove_dot(self, pos):
        tile = self.at(pos)
        if tile != '.':
            self.tmap.set_tile(pos, '.')
            self.tmap.cache_map()
            if tile == '*':
                self.dots_left -= 1

    def draw(self):
        self.tmap.draw()


class Ghost:

    def __init__(self, frame, tile_factory, pos, level):
        tile = tile_factory.get(GHOST_TILE)
        self.sprite = Sprite(frame, tile, pos, speed=2)
        self.level = level
        self.direction = None
        self.set_random_direction()

    def get_possible_moves(self):
        result = []
        directions = [LEFT, RIGHT, UP, DOWN]
        for vector in directions:
            if vector * -1 != self.direction:
                newpos = self.sprite.pos + vector
                tile = self.level.at(newpos)
                if tile != '#':
                    result.append(vector)
        if not result:
            result = [self.direction * (-1)]
        return result

    def set_random_direction(self):
        moves = self.get_possible_moves()
        i = random.randint(0, len(moves) - 1)
        self.direction = moves[i]

    def move(self):
        if self.sprite.finished:
            self.set_random_direction()
            self.sprite.add_move(self.direction)
        else:
            self.sprite.move()

    def update(self):
        self.move()

    def draw(self):
        self.sprite.draw()


class Pac:
        
    def __init__(self, frame, tile_factory, pos, level):
        self.level = level
        self.tile_factory = tile_factory
        tile = tile_factory.get('b.pac_right')
        self.sprite = Sprite(frame, tile, pos, speed=4)
        self.eaten = None
        self.score = 0
        self.buffered_move = None

    def set_direction(self, direction):
        self.sprite.tile = self.tile_factory.get(PAC_TILES[direction])

    def move(self, direction):
        if not self.sprite.finished:
            self.buffered_move = direction
            return
        newpos = self.sprite.pos + direction
        self.set_direction(direction)
        tile = self.level.at(newpos)
        if tile != '#':
            self.sprite.add_move(direction, when_finished=self.try_eating)

    def try_eating(self):
        tile = self.level.at(self.sprite.pos)
        if tile != '.':
            self.level.remove_dot(self.sprite.pos)
            if tile == '*':
                self.score += 100
            else:
                self.score += 1000
            self.eaten = tile

    def update(self):
        """Try eating dots and fruit"""
        if self.sprite.finished and self.buffered_move:
            self.move(self.buffered_move)
            self.buffered_move = None
        if not self.sprite.finished:
            self.sprite.move()

    def draw(self):
        self.sprite.draw()

    def collision(self, sprites):
        for sprite in sprites:
            if self.sprite.pos == sprite.sprite.pos:
                return True

    def die(self):
        self.buffered_move = None
        self.sprite.path = []


class PacGame:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(10, 10, 640, 512))
        self.tile_factory = TileFactory('data/tiles.conf')

        self.level = None
        self.pac = None
        self.ghosts = []
        self.status_box = None
        self.events = None

        self.create_level()
        self.create_pac()
        self.create_ghosts()
        self.create_status_box()
        frame = Frame(self.screen, Rect(660, 220, 200, 200))
        self.lives = BarDisplay(frame, self.tile_factory, 3, 'p')

        self.collided = False
        self.mode = None
        self.update_mode = self.update_ingame

    def create_level(self):
        tmap = TiledMap(self.frame, self.tile_factory)
        self.level = PacLevel(LEVEL, tmap)

    def create_pac(self):
        start_pos = Vector(5, 5)
        self.pac = Pac(self.frame, self.tile_factory, PAC_START, self.level)
        self.pac.set_direction(RIGHT)

    def create_ghosts(self):
        self.ghosts = []
        for pos in GHOST_POSITIONS:
            self.ghosts.append(Ghost(self.frame, self.tile_factory, pos, self.level))

    def reset_level(self):
        self.pac.sprite.pos = PAC_START
        self.create_ghosts()

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 200))
        data = {
            'score': 0,
            'level':1,
            }
        self.status_box = DictBox(frame, data)

    def check_collision(self):
        if self.pac.collision(self.ghosts):
            self.update_mode = self.update_die
            self.pac.die()
            self.collided = True

    def update_die(self):
        """finish movements"""
        if self.pac.sprite.finished:
            time.sleep(1)
            self.lives.decrease()
            if self.lives.value == 0:
                self.events.exit_signalled()
            else:
                self.reset_level()
                self.events.empty_event_queue()
                self.update_mode = self.update_ingame

    def update_level_complete(self):
        """finish movement"""
        if self.pac.sprite.finished:
            time.sleep(1)
            self.events.exit_signalled()

    def update_ingame(self):
        self.check_collision()
        if self.pac.eaten:
            self.status_box.data['score'] = self.pac.score
            self.pac.eaten = None
            self.score = self.pac.score
        if self.level.dots_left == 0:
            self.update_mode = self.update_level_complete

    def draw(self):
        self.update_mode()
        self.level.draw()
        self.pac.update()
        self.pac.draw()
        for g in self.ghosts:
            g.update()
            g.draw()
        self.status_box.draw()
        pygame.display.update()
        self.check_collision()
        time.sleep(0.005)

    def run(self):
        self.mode = self.update_ingame
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.pac.move))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/pac.conf', PacGame)
    game.run()