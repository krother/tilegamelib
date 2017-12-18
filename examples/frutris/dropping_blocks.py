
from tilegamelib import Sprite
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP


class MovingBlocks:

    def __init__(self, level, sprites, chars):
        self.level = level
        self.sprites = sprites
        self.chars = chars

    def drop(self):
        assert self.finished
        newsprites = []
        newchars = []
        for sprite, char in zip(self.sprites, self.chars):
            newpos = sprite.pos + DOWN
            if self.level.tmap.at(newpos) == '.':
                sprite.add_move(DOWN)
                newsprites.append(sprite)
                newchars.append(char)
            else:
                self.level.insert(sprite.pos, char)
        self.sprites = newsprites
        self.chars = newchars

    def move(self):
        for s in self.sprites:
            s.move()

    def draw(self):
        for s in self.sprites:
            s.draw()

    @property
    def finished(self):
        for s in self.sprites:
            if not s.finished:
                return False
        return True


class Diamond(MovingBlocks):

    def __init__(self, game, level, column):
        sprites = [Sprite(game, 'd', (column + 1, 0), speed=4)]
        MovingBlocks.__init__(self, level, sprites, 'd')


class FruitPair(MovingBlocks):

    def __init__(self, game, level, chars=('a', 'b')):
        sprites = [
            Sprite(game, chars[0], (3, 0), speed=4),
            Sprite(game, chars[1], (4, 0), speed=4),
        ]
        MovingBlocks.__init__(self, level, sprites, chars)

    def rotate(self):
        if len(self.sprites) != 2 or not self.finished:
            return
        first, second = self.sprites
        if first.pos[0] == second.pos[0]:
            newpos = [first.pos + UP, second.pos + RIGHT]
            if self.level.are_positions_empty(newpos):
                first.add_move(UP)
                second.add_move(RIGHT)
        else:
            newpos = [first.pos, second.pos + DOWN + LEFT]
            if self.level.are_positions_empty(newpos):
                second.add_move(DOWN + LEFT)
                self.sprites = second, first
                self.chars = self.chars[1], self.chars[0]

    def get_shifted_positions(self, direction):
        return [sprite.pos + direction for sprite in self.sprites]

    def shift(self, direction):
        if self.finished:
            new_positions = self.get_shifted_positions(direction)
            if self.level.are_positions_empty(new_positions):
                for sprite in self.sprites:
                    sprite.add_move(direction)
