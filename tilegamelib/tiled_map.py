
import pygame
import numpy as np

from .vector import ZERO_VECTOR


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

    def is_visible(self, pos):
        """
        Checks if the referenced position is in the visible part of the screen.
        Returns boolean.
        """
        return all(pos >= self.map_pos) and \
               all(pos <= self.map_pos + self.win_size)

    def check_position(self, pos):
        """Checks if the given position is on the map."""
        return all(ZERO_VECTOR <= pos) and all(pos < self.size)

    def at(self, pos):
        """Returns the symbol of the tile at the given position."""
        if self.check_position(pos):
            return self.map[pos[0]][pos[1]]

    def check_move(self, vector):
        """
        Checks if the visible part of the map can be moved by
        the given numpy 2D vector.
        """
        newpos = self.map_pos + vector
        return all(ZERO_VECTOR <= newpos) and \
               all(newpos <= self.size - self.win_size)

    def zoom_to(self, pos):
        """
        Sets the position of the map that the window should zoom in on.
        pos (x,y) are integer indices on the tile map.
        """
        self.map_pos = pos
        self.offset = pos * self.tile_factory.tile_size

    def __str__(self):
        return self.get_map()

    def get_map(self):
        rows = '\n'.join(''.join(row) for row in zip(*self.map))
        return rows

    def set_map(self, data):
        """Creates a 2D map with tiles from a multiline string."""
        rows = data.replace('\r', '').strip().split('\n')
        self.size = np.array([len(rows[0]), len(rows)])
        self.fill_map('.')
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.map[x][y] = rows[y][x]
        self._cache_map()

    def fill_map(self, char, size=None):
        """Creates an empty map."""
        if not size is None:
            self.size = np.array(size)
        self.map = np.chararray(self.size, unicode=True)
        self.map[:] = char

    def draw(self):
        """Draws the map."""
        if self._modified:
            self._cache_map()
        src = pygame.Rect(
            self.offset[0], self.offset[1],
            self.win_size_px[0], self.win_size_px[1]
        )
        dest = pygame.Rect(
            0, 0,
            self.win_size_px[0], self.win_size_px[1])
        self.frame.blit(self.mapsurf, dest, src)

    def get_tile(self, pos):
        return self.tile_factory.get(self.at(pos))

    def set_tile(self, pos, tilename):
        self.map[pos[0]][pos[1]] = tilename
        self._modified = True

    def _cache_map(self):
        self.mapsurf = pygame.Surface(tuple(self.map_size_px))
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                tile = self.get_tile((x, y))
                pos = np.array([tile.size[0] * x, tile.size[1] * y])
                tile.draw(self.mapsurf, pos)
        self._modified = False
