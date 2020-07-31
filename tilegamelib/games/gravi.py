
import random
import arcade
from arcade.sprite import Sprite

from tilegamelib import TiledMap
from tilegamelib.game import Game
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP
from tilegamelib.config import config
from tilegamelib import Vector

MOVE_DELAY = 50

LEVEL = """#################
#.........#...bb#
#.........#.##bb#
#.........#.##..#
#......##a....a.#
#........a.....a#
#...............#
#...............#
#...............#
#...............#
#...............#
#...............#
#################"""

THRUST = {
    LEFT: Vector(-3, 0),
    RIGHT: Vector(+3, 0),
    UP: Vector(0, +3),
    DOWN: Vector(0, -3),
}

config.RESOLUTION = (800, 550)
config.TILE_FILE = 'fruit.csv'
config.GAME_NAME = 'Gravi'

START_POS = (5, 5)
MAP_OFS = Vector(96, 96)
PLAYER_OFS = Vector(96, 448)
SPRITE = 'b.pac_right'

class Level:

    def __init__(self, tiles):
        self.tmap = TiledMap(tiles, LEVEL, offset=MAP_OFS)
        self.place_random_fruit()

    def remove_fruit(self, pos):
        tile = self.tmap.at(pos)
        if tile != '.':
            self.tmap.set(pos, '.')

    def place_random_fruit(self):
        x = random.randint(1, self.tmap.size.x - 2)
        y = random.randint(1, self.tmap.size.y - 2)
        fruit = random.choice('abcdef')
        self.tmap.set((x, y), fruit)

    def draw(self):
        self.tmap.draw()


class Ship:

    def __init__(self, tiles, pos, level):
        self.tiles = tiles
        self.level = level
        self.sprite = tiles[SPRITE]
        self.pos = Vector(50, 50)
        self.vector = Vector(0, 0)
        self.crashed = False
        self.counter = MOVE_DELAY

    def draw(self):
        p = self.pos + PLAYER_OFS
        self.sprite.draw(p.x, p.y, 32, 32)

    def thrust(self, direction):
        self.vector += THRUST[direction]

    def move(self):
        """move and apply gravitation"""
        self.pos = self.pos + self.vector
        self.counter -= 1
        if self.counter <= 0:
            self.counter = MOVE_DELAY
            self.vector += Vector(0, -1)


class Gravi(Game):

    def __init__(self):
        super().__init__()
        self.level = Level(self.tiles)
        self.ship = Ship(self.tiles, START_POS, self.level)
        self.delay = MOVE_DELAY

    def fruit_collision(self):
        return False

    def wall_collision(self):
        return False

    def update(self, time_delta):
        """called by arcade"""
        self.ship.move()
        if self.fruit_collision():
            self.level.remove_fruit(self.ship.sprite.pos)
            print(vec)
            self.level.place_random_fruit()
        if self.wall_collision():
            self.exit()

    def on_draw(self):
        """called by arcade"""
        self.level.draw()
        self.ship.draw()

    def move(self, vec):
        self.ship.thrust(vec)

if __name__ == '__main__':
    snake = Gravi()
    arcade.run()
