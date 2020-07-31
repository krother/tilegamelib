
import random
import arcade
import os

from tilegamelib import TiledMap
from tilegamelib.game import Game
from tilegamelib.sprites import TileSprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP
from tilegamelib.config import config
from tilegamelib import Vector

MOVE_DELAY = 25


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
    str(UP): 'b.pac_up',
    str(DOWN): 'b.pac_down',
    str(LEFT): 'b.pac_left',
    str(RIGHT): 'b.pac_right'
}

EASY = False

config.RESOLUTION = (800, 550)
config.BASE_PATH = os.path.split(__file__)[0] + os.sep
config.TILE_FILE = config.BASE_PATH + 'fruit.csv'
config.GAME_NAME = 'Snake'

START_POS = (5, 5)
MAP_OFS = Vector(96, 96)
PLAYER_OFS = Vector(96, 448)


class SnakeLevel:

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


class SnakeSprite:

    def __init__(self, tiles, pos, level):
        self.tiles = tiles
        self.level = level
        self.head = None
        self.tail = []
        self.tail_waiting = []
        self.head = TileSprite(self.tiles['b.pac_right'], pos, HEAD_SPEED, offset=Vector(96, 448))
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

    def set_direction(self, direction):
        """prevent reverse move"""
        if len(self.tail) > 0 and direction == self.past_directions[0] * -1:
            return
        self.direction = direction
        headtile = HEAD_TILES[str(direction)]
        self.head.tile = self.tiles[headtile]
        if EASY:
            self.move_forward()

    def draw(self):
        """draw head and tail parts"""
        for sp in self.sprites:
            sp.draw()

    def move(self):
        """move head and tail parts"""
        if self.is_moving():
            for sp in self.sprites:
                sp.update()

    @property
    def positions(self):
        return [self.head.pos] + [seg.pos for seg in self.tail]

    def grow(self):
        """fruit has been eaten"""
        segment = TileSprite(self.tiles['b.tail'], self.positions[-1], HEAD_SPEED, offset=PLAYER_OFS)
        self.tail_waiting.append(segment)
        if not self.past_directions:
            self.past_directions.append(self.direction)
        else:
            self.past_directions.append(self.past_directions[-1])

    def move_forward(self):
        """smooth movement finished, compute next step"""
        newpos = self.head.pos + self.direction
        tile = self.level.tmap.at(newpos)
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
            if self.tail:
                self.past_directions = [self.direction] + self.past_directions[:-1]


class SnakeGame(Game):

    def __init__(self):
        super().__init__()
        self.level = SnakeLevel(self.tiles)
        self.snake = SnakeSprite(self.tiles, START_POS, self.level)
        self.update_mode = self.update_ingame
        self.delay = MOVE_DELAY

    def update_finish_moves(self):
        """finish movements before Game Over"""
        if not self.snake.is_moving():
            self.exit()

    def update_ingame(self):
        """game is running"""
        self.delay -= 1
        if self.delay <= 0:
            self.delay = MOVE_DELAY
            if not EASY:
                self.snake.move_forward()
        if self.snake.eaten and not self.snake.is_moving():
            self.level.remove_fruit(self.snake.head.pos)
            self.level.place_random_fruit()
            self.snake.eaten = None
        if self.snake.crashed:
            self.update_mode = self.update_finish_moves

    def update(self, time_delta):
        """called by arcade"""
        self.update_mode()
        self.snake.move()

    def on_draw(self):
        """called by arcade"""
        self.level.draw()
        self.snake.draw()

    def move(self, vec):
        self.snake.set_direction(vec)

def main():
    snake = SnakeGame()
    arcade.run()

if __name__ == '__main__':
    main()
