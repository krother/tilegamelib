
class Ghost:

    def __init__(self, sprite, pos, tmap):
        self.sprite = sprite
        self.map = tmap
        self.lastvec = 0

    def get_possible_moves(self):
        result = []
        directions = [LEFT, RIGHT, UP, DOWN]
        for vector in directions:
            if vector.inverse() != self.lastvec:
                newpos = self.pos + vector
                tile = self.map.at(newpos)
                if tile != '#':
                    result.append(vector)
        if not result:
            result =[self.lastvec.inverse()]

        return result

    def get_random_vector(self):
        moves = self.get_possible_moves()
        i = random.randint(0, len(moves))
        self.lastvec = moves[i]
        return moves[i]
        
    def keep_moving(self):
        if not self.is_moving(): 
            vector = self.get_random_vector()
            self.add_move(vector)


def create_ghost(tile_factory, tmap, pos):
    tile = tile_factory.get('b.ghost')
    sprite = Sprite(context, tmap.frame, tile, pos, speed=4)
    ghost = Ghost(sprite, pos, tmap)

