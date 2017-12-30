
import random
import time

import pygame
from pygame import K_SPACE, Rect, mask
from pygame.sprite import Sprite, Group, groupcollide, collide_mask

from tilegamelib import AnimatedTile, TiledMap
from tilegamelib.bar_display import BarDisplay
from tilegamelib.basic_boxes import DictBox
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.game import Game
from tilegamelib.vector import DOWN, LEFT, RIGHT, UP, Vector


MIN_X = -16
MAX_X = 764


class Player(Sprite):

    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.tile = game.get_tile('rot.hoch')
        self.image = self.tile.image.subsurface(self.tile.box)
        self.g = Group(self)
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
        self.rect = Rect(self.pos.x, self.pos.y, 32, 32)
        self.g.draw(self.game.screen.display)


class Alien(Sprite):

    def __init__(self, game, pos, speed=1, tile='b.ghost_d'):
        Sprite.__init__(self)
        self.game = game
        self.tile = game.get_tile(tile)
        self.image = self.tile.image.subsurface(self.tile.box)
        self.pos = pos
        self.speed = speed
        self.direction = RIGHT
        self.down_count = 0
        self.next_direction = None

    def update(self):
        """Alien movement logic"""
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
        self.rect = Rect(self.pos.x, self.pos.y, 32, 32)


class Shot(Sprite):

    def __init__(self, game, pos, speed=4):
        Sprite.__init__(self)
        self.game = game
        self.tile = game.get_tile('b.dot')
        self.image = self.tile.image.subsurface(self.tile.box)
        self.mask = mask.from_surface(self.image)
        self.pos = Vector(pos)
        self.speed = speed

    def update(self):
        self.pos += UP * self.speed
        self.rect = Rect(self.pos.x, self.pos.y, 32, 32)


class InvadersGame:

    def __init__(self):
        self.game = Game()
        floorframe = Frame(self.game.screen, Rect(0, 542, MAX_X + 36, 596))
        self.floor = TiledMap(self.game, floorframe)
        self.floor.fill_map('#', (25, 2))
        self.player = Player(self.game)
        self.aliens = Group()
        self.shots = Group()
        self.create_aliens()

    def create_aliens(self):
        for i in range(4):
            for j in range(20):
                alien = Alien(self.game, Vector(j * 32 + 32, i * 64))
                self.aliens.add(alien)

    def shoot(self):
        shot = self.player.get_shot()
        self.shots.add(shot)

    def draw(self):
        self.game.screen.clear()
        self.floor.draw()
        self.player.move()
        self.player.draw()
        self.shots.update()
        self.shots.draw(self.game.screen.display)
        self.aliens.update()
        self.aliens.draw(self.game.screen.display)
        groupcollide(self.shots, self.aliens, True, True, collided=collide_mask)
        if not self.aliens:
            self.game.exit()

    def run(self):
        self.game.event_loop(figure_moves=self.player.set_direction,
            draw_func=self.draw, keymap={K_SPACE: self.shoot})


if __name__ == '__main__':
    config.FRAME = Rect(10, 10, 640, 512)
    inv = InvadersGame()
    inv.run()
    pygame.quit()
