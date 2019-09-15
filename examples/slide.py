
import arcade
from tilegamelib.game import Game
from tilegamelib import TiledMap
from tilegamelib import MapMove
from tilegamelib import Vector
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from tilegamelib.sprites import TileSprite
from tilegamelib.config import config
from tilegamelib import PLAYER_MOVES
from arcade.key import SPACE

BOXMAP = """##########
#..#...cd#
#a.#.##dc#
#..#.##..#
##g....b.#
#.g..a..b#
#......c.#
##########"""

config.RESOLUTION = (450, 400)
config.TILE_FILE = 'fruit.csv'
config.GAME_NAME = "Slider"

PLAYER_MOVES[SPACE] = 'pickup'
MOVABLE = 'abcdefg'

class Boxes(Game):

    def __init__(self):
        super().__init__()
        self.tm = TiledMap(self.tiles, BOXMAP, offset=Vector(96, 96))
        self.player = TileSprite(self.tiles['frame'], (4, 1), speed=4, offset=Vector(96, 320))
        self.moves = None
        self.block = None
        self.block_sprite = None

    def on_draw(self):
        self.tm.draw()
        if self.block_sprite:
            self.block_sprite.draw()
        self.player.draw()

    def pickup_block(self):
        block = self.tm.at(self.player.pos)
        if block in MOVABLE:
            self.block = block
            self.block_sprite = TileSprite(self.tiles[block], self.player.pos, speed=4, offset=Vector(94, 318))
            self.tm.set(self.player.pos, '.')

    def release_block(self):
        self.tm.set(self.block_sprite.pos, self.block)
        self.block = None
        self.block_sprite = None

    def move_frame(self, direction):
        nearpos = self.player.pos + direction
        if self.tm.is_on_map(nearpos):
            self.player.add_move(direction)
            self.moves = [self.player]

    def move(self, direction):
        if self.moves:
            return
        if direction == 'pickup':
            if self.block:
                self.release_block()
            else:
                self.pickup_block()
            return
        if self.block:
            self.slide_block(direction)
        else:
            self.move_frame(direction)

    def slide_block(self, direction):
        pos = self.player.pos
        nearpos = pos + direction
        while self.tm.at(nearpos) == '.':
            self.player.add_move(direction)
            self.block_sprite.add_move(direction)
            nearpos = nearpos + direction
        self.moves = [self.player, self.block_sprite]

    def update(self, time_delta):
        if self.moves:
            for m in self.moves:
                m.update()
            if self.moves[0].finished:
                self.moves = None
                if self.block:
                    self.check_pairs()
                    self.check_complete()

    def check_pairs(self):
        found = False
        for direction in [UP, DOWN, LEFT, RIGHT]:
            target = self.block_sprite.pos + direction
            b = self.tm.at(target)
            if b == self.block:
                found = True
                self.tm.set(target, '.')
        if found:
            self.block = None
            self.block_sprite = None

    def check_complete(self):
        s = self.tm.get_map()
        if sum([s.count(m) for m in MOVABLE]) == 0:
            self.exit()


if __name__ == '__main__':
    boxes = Boxes()
    arcade.run()
