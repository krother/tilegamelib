
import random
import time

import pygame
from pygame import K_SPACE, Rect, mask
from pygame.sprite import Sprite, Group, groupcollide, collide_mask, spritecollideany

from tilegamelib import AnimatedTile, TiledMap
from tilegamelib.bar_display import BarDisplay
from tilegamelib.basic_boxes import DictBox
from tilegamelib.config import config
from tilegamelib.frame import Frame
from tilegamelib.game import Game
from tilegamelib.vector import DOWN, LEFT, RIGHT, UP, Vector


MIN_X = -8
MAX_X = 772

ALIEN_SHOT_PROBABILITY = 0.002


class Player(Sprite):

    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = game.get_tile_surface('rot.hoch')
        self.mask = mask.from_surface(self.image)
        self.g = Group(self)
        self.pos = Vector(300, 510)
        self.speed = 4
        self.direction = RIGHT

    def set_direction(self, direction):
        if direction in [LEFT, RIGHT]:
            self.direction = direction

    def get_shot(self):
        return Shot(self.game, (self.pos.x, self.pos.y - 16), UP)

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

    def __init__(self, game, pos, direction=RIGHT, speed=1, tile='b.ghost_d'):
        Sprite.__init__(self)
        self.game = game
        self.image = game.get_tile_surface(tile)
        self.pos = pos
        self.speed = speed
        self.direction = direction
        self.down_count = 0
        self.next_direction = None

    def get_shot(self):
        if random.randint(1, 1000) <= ALIEN_SHOT_PROBABILITY * 1000:
            return Shot(self.game, (self.pos.x, self.pos.y), DOWN)

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

    def __init__(self, game, pos, direction, speed=4):
        Sprite.__init__(self)
        self.game = game
        self.image = game.get_tile_surface('b.dot')
        self.mask = mask.from_surface(self.image)
        self.pos = Vector(pos)
        self.direction = direction
        self.speed = speed

    @property
    def rect(self):
        return Rect(self.pos.x, self.pos.y, 32, 32)

    def update(self):
        self.pos += self.direction * self.speed
        if self.pos.y < -32 or self.pos.y > 600:
            self.kill()


class InvadersGame:

    def __init__(self):
        self.game = Game()
        floorframe = Frame(self.game.screen, Rect(0, 542, MAX_X + 36, 596))
        self.floor = TiledMap(self.game, floorframe)
        self.floor.fill_map('#', (25, 2))
        self.player = Player(self.game)
        self.aliens = Group()
        self.create_aliens()
        self.shots = Group()
        self.alien_shots = Group()

    def create_aliens(self):
        for i in range(4):
            for j in range(20):
                direction = [LEFT, RIGHT][i % 2]
                alien = Alien(self.game, Vector(j * 32 + 32, i * 64), direction)
                self.aliens.add(alien)

    def shoot(self):
        shot = self.player.get_shot()
        self.shots.add(shot)

    def draw(self):
        self.game.screen.clear()
        self.player.draw()
        self.shots.draw(self.game.screen.display)
        self.alien_shots.draw(self.game.screen.display)
        self.aliens.draw(self.game.screen.display)
        self.floor.draw()

    def update(self):
        self.player.move()
        self.shots.update()
        self.alien_shots.update()
        self.aliens.update()
        for a in self.aliens:
            shot = a.get_shot()
            if shot:
                self.alien_shots.add(shot)
        self.draw()
        groupcollide(self.shots, self.aliens, True, True, collided=collide_mask)
        if spritecollideany(self.player, self.alien_shots, collided=collide_mask):
            self.game.exit()
        if not self.aliens:
            self.game.exit()

    def run(self):
        self.game.event_loop(figure_moves=self.player.set_direction,
            draw_func=self.update, keymap={K_SPACE: self.shoot})


if __name__ == '__main__':
    config.FRAME = Rect(10, 10, 640, 512)
    inv = InvadersGame()
    inv.run()
    pygame.quit()
