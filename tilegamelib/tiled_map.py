
import arcade
from arcade import load_texture
import pandas as pd
from .vector import Vector, ZERO_VECTOR
from .config import config


def load_tiles(filename):
    df = pd.read_csv(filename)
    df['path'] = config.BASE_PATH + df['path']
    tiles = {name: load_texture(*cols) for name, *cols in df.values}
    return tiles


class TiledMap:
    """
    A map consisting of 2D-tiles. The map can be scrolled
    in a way that only a part of the map is displayed.
    """
    def __init__(self, tiles, map_str, offset=ZERO_VECTOR):
        self.tiles = tiles
        self.map = [list(row) for row in map_str.strip().split('\n')]
        self.offset = Vector(offset)
        self.map_pos = ZERO_VECTOR
        self._sprites = arcade.SpriteList()
        self._cache_map()

    @property
    def size(self):
        return Vector(len(self.map[0]), len(self.map))

    @property
    def map_size_px(self):
        """size of the map in pixels (x,y)."""
        return self.size * config.TILE_SIZE

    def pos_in_pixels(self, pos):
        """Returns the position in pixels (x,y) of the given tile pos."""
        #(pos - self.map_pos) * config.TILE_SIZE
        pixelpos = Vector(pos.x * 32, (self.size.y - pos.y - 1) * 32)
        return pixelpos + self.offset

    def is_on_map(self, pos):
        """
        Returns True if the referenced position is
        within the map
        """
        pos = Vector(pos)
        boundary = self.map_pos + self.win_size
        return 0 <= pos.x <= boundary.x and \
               0 <= pos.y <= boundary.y

    def is_on_map(self, pos):
        """
        Returns Checks if the given position is on the map."""
        pos = Vector(pos)
        return 0 <= pos.x < self.size.x and \
               0 <= pos.y < self.size.y

    def at(self, pos):
        """Returns the symbol of the tile at the given position."""
        pos = Vector(pos)
        if self.is_on_map(pos):
            return self.map[pos.y][pos.x]

    def get_tile(self, pos):
        """Returns texture at given position"""
        return self.tiles[self.at(pos)]

    def check_move(self, vector):
        """
        Checks if the visible part of the map can be moved by
        the given 2D vector.
        """
        newpos = self.map_pos + vector
        return 0 <= newpos.x <= self.size.x and \
               0 <= newpos.y <= self.size.y

    def zoom_to(self, pos):
        """
        Sets the position of the map that the window should zoom in on.
        pos (x,y) are integer indices on the tile map.
        """
        self.map_pos = Vector(pos)
        self.offset = self.map_pos * config.TILE_SIZE

    def __str__(self):
        return self.get_map()

    def get_map(self):
        rows = '\n'.join(''.join(row) for row in self.map)
        return rows

    def set_map(self, data):
        """Creates a 2D map with tiles from a multiline string."""
        self.map = data.replace('\r', '').strip().split('\n')
        self._cache_map()

    def fill_map(self, char, size=None):
        """Creates an empty map filled with a single character."""
        if size is not None:
            self.size = Vector(size)
        self.map = [[char for x in range(self.size.x)] for y in range(self.size.y)]
        self._cache_map()

    def _cache_map(self):
        self._sprites = arcade.SpriteList()
        for x in range(self.size.x):
            for y in range(self.size.y):
                pos = Vector(x, y)
                # reverse pixel y axis, because arcade starts counting at bot left
                pxpos = self.pos_in_pixels(pos)
                # UNKNOWN: does not work without loading dummy image
                sprite = arcade.Sprite(config.DATA_PATH + '/fruit.xpm', 1) # "images/character.png", 1)
                tile = self.tiles[self.map[pos.y][pos.x]]
                sprite.append_texture(tile)
                sprite.set_texture(1)
                sprite.center_x = pxpos.x
                sprite.center_y = pxpos.y
                self._sprites.append(sprite)

    def draw(self):
        """Draws the map."""
        self._sprites.draw()

    def set(self, pos, tile):
        """Sets the symbol at the given position"""
        pos = Vector(pos)
        self.map[pos.y][pos.x] = tile
        self._cache_map()
