

from tilegamelib.sprites import Sprite
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT

class Pac(Sprite):

    pac_moves = {
        'left': (LEFT, 'b.pac_left'),
        'right': (RIGHT, 'b.pac_right'),
        'up': (UP, 'b.pac_up'),
        'down': (DOWN, 'b.pac_down'),
        }
        
    def __init__(self, context, pos, amap):
        self.map = amap
        tile = context.tile_factory.get('b.pac_right')
        Sprite.__init__(self,context, self.map.frame, tile, pos.copy(), speed=4)
        self.lives = LifeDisplay(self.context, frame, 3, 'p')
        self.dots_eaten = 0

    def create_pac(self):
        self.pac = Pac(self.context, self.level.pac_pos, self.map)
        self.sprites.append(pac)

    def handle_command(self, command):
        if self.is_moving():
            return False
        vec, tilename = self.pac_moves.get(command,(None,None))
        if vec!=None:
            newpos = self.pos + vec
            self.tile = self.tile_factory.get(tilename)
            tile = self.map.at(newpos)
            if tile != '#':
                self.add_move(vec)
                if tile == 'a':
                    return True

    def move_finished(self):
        """Try eating dots and fruit"""
        Sprite.move_finished(self)
        tile = self.map.at(self.pos)
        if tile != '.':
            self.map.set_tile(self.pos, '.')
            self.map.cache_map()
            if tile == 'a':
                self.callback.dot_eaten()
            else:
                self.callback.fruit_eaten()


    def collision(self, sprites):
        for sprite in self.sprites:
            if self.pac.pos == sprite.pos:
                self.lives.lose_one()
                return True

    def dot_eaten(self):
        self.dots_eaten += 1
        self.status_box.data['score'] += 10

    def fruit_eaten(self):
        self.status_box.data['score'] += 100

