
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
from slide_levels import LEVELS

config.RESOLUTION = (1000, 800)
config.TILE_FILE = 'fruit.csv'
config.GAME_NAME = "Slider"

PLAYER_MOVES[SPACE] = 'pickup'
MOVABLE = 'abcdefg'
MAP_OFFSET = Vector(96, 96)

class Boxes(Game):

    def __init__(self):
        super().__init__()
        self.level = 0
        self.tm = None
        self.player = None
        self.moves = None
        self.block = None
        self.block_sprite = None
        self.next_level()

    @property
    def sprite_offset(self):
        return MAP_OFFSET + Vector(0, 32 * self.tm.size.y - 32)

    def next_level(self):
        self.tm = TiledMap(self.tiles, LEVELS[self.level], offset=MAP_OFFSET)
        self.player = TileSprite(self.tiles['frame'], (1, 1), speed=4, offset=self.sprite_offset)
        self.moves = None
        self.block = None
        self.block_sprite = None
        self.level += 1

    def on_draw(self):
        self.tm.draw()
        if self.block_sprite:
            self.block_sprite.draw()
        self.player.draw()

    def pickup_block(self):
        block = self.tm.at(self.player.pos)
        if block in MOVABLE:
            self.block = block
            self.block_sprite = TileSprite(self.tiles[block], self.player.pos, speed=4, offset=self.sprite_offset)
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
            if self.level == len(LEVELS):
                self.exit()
            else:
                self.next_level()


if __name__ == '__main__':
    boxes = Boxes()
    arcade.run()
