
import json
import os

from pygame import image

from .config import config
from .tiles import Tile
from .vector import Vector


class NoTileError(Exception):
    pass


class TileFactory:
    """
    Manages a set of tiles.
    """
    def __init__(self):
        self.tiles = {}
        self.tile_size = Vector(config.TILE_SIZE)
        self.path = ''
        self.parse_config(config.TILE_SPECS)

    def parse_config(self, config_filename):
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        conf = json.loads(open(config_filename).read())
        self.tile_size = conf['tile_size']
        for tileset in conf['tilesets'].values():
            self.load_tiles(tileset)
        self.add_tile_synonyms(conf['synonyms'])

    def load_tiles(self, tileset):
        """Loads tile graphics from a file."""
        img = image.load(self.path + tileset['filename']).convert_alpha()
        for xpos, ypos, name in tileset['tiles']:
            index = (int(xpos), int(ypos))
            self.tiles[name] = Tile(name, index, self.tile_size, img)

    def add_tile_synonyms(self, synonyms):
        for abbrev in synonyms:
            self.tiles[abbrev] = self.get(synonyms[abbrev])

    def get(self, key):
        """Returns a Tile instance."""
        result = self.tiles.get(key, None)
        if not result:
            raise NoTileError("No such tile: %s" % str(key))
        return result

    def get_surface(self, key):
        """Returns a pygame.Surface instance."""
        tile = self.get(key)
        return tile.image.subsurface(tile.box)
