
import pygame
from pygame import Rect

from .config import config
from .vector import ZERO_VECTOR, Vector


class TiledMap:
    """
    A map consisting of 2D-tiles. The map can be scrolled
    in a way that only a part of the map is displayed.
    """
    def __init__(self, game, frame=None):
        self.frame = frame or game.frame
        self.tile_factory = game.tile_factory
        self.offset = ZERO_VECTOR
        self.map_pos = ZERO_VECTOR
        self.size = ZERO_VECTOR
        self.map = []
        self.mapsurf = None
        self._modified = True

    @property
    def win_size_px(self):
        """size of the map window in pixels (x,y)."""
        return self.win_size * self.tile_factory.tile_size

    @property
    def map_size_px(self):
        """size of the map in pixels (x,y)."""
        return self.size * self.tile_factory.tile_size

    @property
    def win_size(self):
        """size of the window in tiles (rounded down)."""
        return self.frame.size // self.tile_factory.tile_size

    def pos_in_pixels(self, pos):
        """Returns the position in pixels (x,y) of the given tile pos."""
        return (pos - self.map_pos) * self.tile_factory.tile_size

    def is_on_screen(self, pos):
        """
        Returns True if the referenced position is
        in the visible part of the screen.
        """
        pos = Vector(pos)
        boundary = self.map_pos + self.win_size
        return self.map_pos.x <= pos.x <= boundary.x and \
               self.map_pos.y <= pos.y <= boundary.y

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

    def check_move(self, vector):
        """
        Checks if the visible part of the map can be moved by
        the given 2D vector.
        """
        newpos = self.map_pos + vector
        boundary = self.size + self.win_size
        return 0 <= newpos.x <= boundary.x and \
               0 <= newpos.y <= boundary.y

    def zoom_to(self, pos):
        """
        Sets the position of the map that the window should zoom in on.
        pos (x,y) are integer indices on the tile map.
        """
        self.map_pos = Vector(pos)
        self.offset = self.map_pos * self.tile_factory.tile_size

    def __str__(self):
        return self.get_map()

    def get_map(self):
        rows = '\n'.join(''.join(row) for row in self.map)
        return rows

    def set_map(self, data):
        """Creates a 2D map with tiles from a multiline string."""
        rows = data.replace('\r', '').strip().split('\n')
        self.size = Vector(len(rows[0]), len(rows))
        self.fill_map('.')
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                self.map[y][x] = char
        self._cache_map()

    def fill_map(self, char, size=None):
        """Creates an empty map filled with a single character."""
        if size is not None:
            self.size = Vector(size)
        self.map = [[char for x in range(self.size.x)] for y in range(self.size.y)]
        # self.map = np.chararray(self.size, unicode=True)  # abandoned NumPy dependency

    def draw(self):
        """Draws the map."""
        if self._modified:
            self._cache_map()
        src = pygame.Rect(
            self.offset.x, self.offset.y,
            self.win_size_px.x, self.win_size_px.y
        )
        dest = pygame.Rect(
            0, 0,
            self.win_size_px.x, self.win_size_px.y)
        self.frame.blit(self.mapsurf, dest, src)

    def get_tile(self, pos):
        """Returns the symbol at the given position"""
        return self.tile_factory.get(self.at(pos))

    def get_tile_surface(self, pos):
        """Returns the symbol at the given position"""
        return self.tile_factory.get_surface(self.at(pos))

    def set_tile(self, pos, tilename):
        """Sets the symbol at the given position"""
        pos = Vector(pos)
        self.map[pos.y][pos.x] = tilename
        self._modified = True

    def _cache_map(self):
        """used internally to pre-calculate map graphics"""
        self.mapsurf = pygame.Surface(tuple(self.map_size_px))
        for x in range(self.size.x):
            for y in range(self.size.y):
                pos = Vector(x, y)
                pixelpos = pos * config.TILE_SIZE
                tile = self.get_tile_surface(pos)
                rect = Rect(pixelpos.x, pixelpos.y, tile.get_width(), tile.get_height())
                self.mapsurf.blit(tile, rect)
                # tile = self.get_tile(pos)
                # pixelpos = tile.size * pos
                # tile.draw(self.mapsurf, pixelpos)
        self._modified = False
