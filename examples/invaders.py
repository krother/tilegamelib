
import random
import time

import pygame
from pygame import K_SPACE, Rect

from tilegamelib import AnimatedTile, TiledMap
from tilegamelib.bar_display import BarDisplay
from tilegamelib.basic_boxes import DictBox
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.game import Game
from tilegamelib.sprites import Sprite
from tilegamelib.vector import DOWN, LEFT, RIGHT, UP, Vector


MIN_X = -16
MAX_X = 764


class Player:

    def __init__(self, game):
        self.game = game
        self.tile = game.get_tile('rot.hoch')
        self.pos = Vector(300, 500)
        self.speed = 4
        self.direction = RIGHT

    def set_direction(self, direction):
        if direction in [LEFT, RIGHT]:
            self.direction = direction

    def get_shot(self):
        return Shot(self.game, (self.pos.x, self.pos.y - 16))

    def move(self):
        self.pos += self.direction * self.speed
        if self.pos.x < MIN_X:
            self.pos.x = MIN_X
        elif self.pos.x > MAX_X:
            self.pos.x = MAX_X

    def draw(self):
        self.tile.draw(self.game.frame, self.pos)


class Alien:

    def __init__(self, game, pos, speed=1, tile='b.ghost_d'):
        self.game = game
        self.tile = game.get_tile(tile)
        self.pos = pos
        self.speed = speed
        self.direction = RIGHT
        self.down_count = 0
        self.next_direction = None
        self.hit = False

    def move(self):
        self.pos += self.direction * self.speed
        if self.pos.x < MIN_X:
            self.pos.x = MIN_X
            self.direction = DOWN
            self.down_count = 32
            self.next_direction = RIGHT
        elif self.pos.x > MAX_X:
            self.pos.x = MAX_X
            self.direction = DOWN
            self.down_count = 32
            self.next_direction = LEFT
        if self.down_count > 0:
            self.down_count -= self.speed
            if self.down_count <= 0:
                self.direction = self.next_direction

    def draw(self):
        self.tile.draw(self.game.frame, self.pos)

    def explode(self):
        self.hit = True

    @property
    def expired(self):
        return self.hit


class Shot:

    def __init__(self, game, pos, speed=4):
        self.game = game
        self.tile = game.get_tile('b.dot')
        self.pos = Vector(pos)
        self.speed = speed
        self.hit = False

    def move(self):
            self.pos += UP * self.speed

    def draw(self):
        self.tile.draw(self.game.frame, self.pos)

    def collision(self, object):
        return self.pos.x - 16 < object.pos.x < self.pos.x + 16 and \
           self.pos.y - 16 < object.pos.y < self.pos.y + 16


    @property
    def expired(self):
        return self.hit or self.pos.y < -20


class InvadersGame:

    def __init__(self):
        self.game = Game()
        floorframe = Frame(self.game.screen, Rect(0, 542, MAX_X + 36, 596))
        #self.bg = TiledMap(self.game, floorframe)
        self.floor = TiledMap(self.game, floorframe)
        #self.bg.fill_map('#', (25, 2))
        self.floor.fill_map('#', (25, 2))
        self.player = Player(self.game)
        self.aliens = []
        self.shots = []
        self.create_aliens()

    def create_aliens(self):
        for i in range(4):
            for j in range(20):
                alien = Alien(self.game, Vector(j * 32 + 32, i * 64))
                self.aliens.append(alien)

    def shoot(self):
        shot = self.player.get_shot()
        self.shots.append(shot)

    def check_collisions(self):
        for s in self.shots:
            for a in self.aliens:
                if s.collision(a):
                    a.explode()
                    s.hit = True

    def draw(self):
        self.game.screen.clear()
        self.floor.draw()
        self.player.move()
        self.player.draw()
        for s in self.shots:
            s.move()
            s.draw()
        for a in self.aliens:
            a.move()
            a.draw()
        self.check_collisions()
        self.aliens = [a for a in self.aliens if not a.expired]
        self.shots = [s for s in self.shots if not s.expired]
        if len(self.aliens) == 0:
            self.game.exit()

    def run(self):
        self.game.event_loop(figure_moves=self.player.set_direction,
            draw_func=self.draw, keymap={K_SPACE: self.shoot})


if __name__ == '__main__':
    config.FRAME = Rect(10, 10, 640, 512)
    inv = InvadersGame()
    inv.run()
    pygame.quit()
