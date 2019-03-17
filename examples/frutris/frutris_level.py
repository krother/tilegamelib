
from tilegamelib import TiledMap
from tilegamelib.animation import AnimatedTile
from tilegamelib.map_move import MapMove
from tilegamelib.move_group import MoveGroup
from tilegamelib.vector import DOWN
from tilegamelib.vector import LEFT
from tilegamelib.vector import RIGHT
from tilegamelib.vector import UP, Vector

from multiplets import FruitMultiplets

EXPLOSION = ['b.explo_1', 'b.explo_2', 'b.explo_3', 'b.explo_4',
             'b.explo_5', 'b.explo_6', 'b.empty']


class FrutrisLevel:

    def __init__(self, game, level):
        self.tmap = TiledMap(game)
        self.tmap.set_map(level)

    def insert(self, pos, fruit):
        self.tmap.set_tile(pos, fruit)

    def is_pos_in_box(self, pos):
        if (0 <= pos.x < self.tmap.size.x) and \
           (0 <= pos.y < self.tmap.size.y):
            return True

    def are_positions_empty(self, positions):
        for pos in positions:
            if self.tmap.at(pos) != '.':
                return False
        return True

    def trace_multiplets(self, pos, trace, char, taboo):
        """Recursively looks for quartets of identical bricks."""
        if not self.is_pos_in_box(pos) \
            or pos in taboo \
            or self.tmap.at(pos) != char or pos in trace:
            return
        trace.add(pos)
        self.trace_multiplets(pos + LEFT, trace, char, taboo)
        self.trace_multiplets(pos + RIGHT, trace, char, taboo)
        self.trace_multiplets(pos + DOWN, trace, char, taboo)

    def find_multiplets(self):
        """Returns a list of multiplet positions"""
        multiplets = FruitMultiplets()
        taboo = []
        for x in range(1, self.tmap.size.x - 1):
            for y in range(self.tmap.size.y):
                pos = Vector(x, y)
                if self.tmap.at(pos) in ('.', '#'):
                    continue
                found = set()
                char = self.tmap.at(pos)
                self.trace_multiplets(pos, found, char, taboo)
                if len(found) >= 4:
                    multiplets.add_multiplet(found)
                    taboo.extend(found)
        return multiplets

    def get_dropped_bricks(self):
        moves = []
        for x in range(self.tmap.size.x):
            pos = Vector(x, self.tmap.size.y - 1)
            while pos.y > 0:
                pos_above = pos + UP
                if self.tmap.at(pos) == '.' and self.tmap.at(pos_above) != '.':
                    moves.append(MapMove(self.tmap, pos_above, DOWN, speed=4))
                pos = pos_above
        return MoveGroup(moves)

    def get_explosions(self, multiplets):
        explosions = []
        for pos in multiplets.get_positions():
            self.tmap.set_tile(pos, '.')
            explosions.append(AnimatedTile(EXPLOSION, self.tmap.tile_factory, self.tmap.frame, pos))
        if len(explosions) == 0:
            return None
        explosions = MoveGroup(explosions)
        return explosions

    def box_overflow(self):
        if self.get_stack_size() == self.tmap.size.y - 1:
            return True

    def get_stack_size(self):
        """Returns height of the fruit stack."""
        y = 0
        while y < self.tmap.size.y:
            for x in range(1, self.tmap.size.x - 1):
                char = self.tmap.at((x, y))
                if char != '.':
                    return self.tmap.size.y - y - 1
            y += 1
        return 0

    def draw(self):
        self.tmap.draw()
