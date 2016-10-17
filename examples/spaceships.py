#! /usr/bin/python

from tilegamelib.vector import Vector, UP, DOWN, LEFT, RIGHT
from tilegamelib.frame import Frame
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.basic_boxes import DictBox
from tilegamelib.tile_factory import TileFactory
from tilegamelib.tiled_map import TiledMap
from tilegamelib.events import EventGenerator
from tilegamelib.event_listener import EventListener
from pygame import Rect, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE
import random
import time
import pygame

MOVE_DELAY = 50

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
#.................@#
####################"""

MOVE_OK = 1
MOVE_CRASH = 2
HEAD_SPEED = 4

HEAD_TILES = {
    UP: 'rot.hoch',
    DOWN: 'rot.runter',
    LEFT: 'rot.links',
    RIGHT: 'rot.rechts'
    }


class SpaceshipLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.tmap.cache_map()

    def at(self, pos):
        return self.tmap.at(pos)

    def place_random_mines(self, n=20):
        for i in range(n):
            x = random.randint(2, self.tmap.size.x - 3)
            y = random.randint(1, self.tmap.size.y - 2)
            self.tmap.set_tile(Vector(x, y), "+")
        self.tmap.cache_map()

    def draw(self):
        self.tmap.draw()


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
        tile = self.tile_factory.get('rot.runter')
        self.sprite = Sprite(self.frame, tile, pos, HEAD_SPEED)

    def set_direction(self, direction):
        self.direction = direction
        headtile = HEAD_TILES[direction]
        self.sprite.tile = self.tile_factory.get(headtile)
         
    def draw(self):
        if self.is_moving():
            self.sprite.move()
        else:
            self.sprite.draw()
            
    @property
    def position(self):
        return self.sprite.pos

    def move_forward(self):
        newpos = self.sprite.pos + self.direction
        tile = self.level.at(newpos)
        self.sprite.add_move(self.direction)
        if tile in ('#', '+'):
            self.crashed = True
        elif tile == "@":
            self.finished = True
        
    def left(self):
        self.set_direction(LEFT)

    def right(self):
        self.set_direction(RIGHT)
        
    def up(self):
        self.set_direction(UP)

    def down(self):
        self.set_direction(DOWN)
        

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
        self.create_spaceship()
        self.create_status_box()

        self.update_mode = self.update_ingame
        self.move_delay = MOVE_DELAY
        self.delay = MOVE_DELAY
        # KEY_REPEAT = GAME_KEY_REPEAT

    def create_spaceship(self):
        start_pos = Vector(1, 1)
        frame = Frame(self.screen, Rect(10, 10, 640, 512))
        self.spaceship = SpaceshipSprite(frame, self.tile_factory, start_pos, self.level)
        self.spaceship.set_direction(DOWN)
        
    def create_level(self):
        frame = Frame(self.screen, Rect(10, 10, 640, 512))
        tmap = TiledMap(frame, self.tile_factory)
        self.level = SpaceshipLevel(LEVEL, tmap)
        self.level.place_random_mines()

    def create_status_box(self):
        frame = Frame(self.screen, Rect(660, 20, 200, 200))
        self.status_box = DictBox(frame, {'score':0})

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.spaceship.is_moving():
            pygame.display.update()
            time.sleep(1)
            self.events.exit_signalled()

    def update_ingame(self):
        self.delay -= 1
        if self.delay <=0:
            self.delay = self.move_delay
            self.spaceship.move_forward()
        if self.spaceship.crashed:
            self.update_mode = self.update_finish_moves
            self.score = 0 
        if self.spaceship.finished:
            self.update_mode = self.update_finish_moves
            self.score = 1000;

    def update(self):
        self.update_mode()
        self.level.draw()
        self.spaceship.draw()
        self.status_box.draw()
        pygame.display.update()
        time.sleep(0.01)

    def exit(self):
        self.events.exit_signalled()

    def get_listener(self):
        listener = EventListener(keymap = {
            K_LEFT: self.spaceship.left,
            K_RIGHT: self.spaceship.right,
            K_UP: self.spaceship.up,
            K_DOWN: self.spaceship.down,
            K_ESCAPE: self.exit
            })
        return listener

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(self.get_listener())
        self.events.add_callback(self)
        self.events.event_loop()

if __name__ == '__main__':
    game = Game('data/snake.conf', SpaceRaceGame)
    game.run()

