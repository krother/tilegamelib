
import time
from tilegamelib.tiled_map import TiledMap


class BarDisplay:

    def __init__(self, tiles, tile_name, value, offset, vertical=False):
        self.map = TiledMap(tiles, tile_name * value, offset=offset)
        self.value = value
        self.tile_name = tile_name
        self.vertical = vertical

    def redraw(self):
        if self.vertical:
            self.map.set_map('\n'.join([self.tile_name] * self.value))
        else:
            self.map.set_map(self.tile_name * self.value)

    def draw(self):
        self.map.draw()

    def increase(self):
        self.value += 1
        self.redraw()

    def decrease(self):
        if self.value > 0:
            self.value -= 1
        self.redraw()
