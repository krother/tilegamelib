
from tilegamelib import TiledMap
from tilegamelib import Vector


class Inventory(TiledMap):

    def __init__(self, tiles, offset, rows=3, cols=4, grid_tile='s'):
        self.n_slots = rows * cols
        self.cols = cols
        slots = "\n".join([grid_tile * cols] * rows)
        super().__init__(tiles, slots, offset=offset)
        self.items = []

    @property
    def full(self):
        return len(self.items) >= self.n_slots

    def add(self, item):
        if not self.full:
            self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    def contains(self, item):
        return item in self.items

    def draw(self):
        super().draw()
        for i, item in enumerate(self.items):
            x = i % self.cols
            y = i // self.cols
            pos = self.pos_in_pixels(Vector(x, y))
            self.tiles[item].draw(pos.x, pos.y, 32, 32)
