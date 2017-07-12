
import pygame

from .vector import Vector


class TiledMap:
    """
    A map consisting of 2D-tiles. The map can be scrolled
    in a way that only a part of the map is displayed.
    """
    def __init__(self, frame, tile_factory):
        self.frame = frame
        self.tile_factory = tile_factory
        self.offset = Vector(0, 0)
        self.map_pos = Vector(0, 0)
        self.size = Vector(0, 0)
        self.map = []
        self.mapsurf = None

    @property
    def win_size_px(self):
        """size of the map window in pixels (x,y)."""
        return self.win_size * self.tile_factory.tile_size.x

    @property
    def map_size_px(self):
        """size of the map in pixels (x,y)."""
        return self.size * self.tile_factory.tile_size.x

    @property
    def win_size(self):
        """size of the window in tiles."""
        x = self.frame.size.x / self.tile_factory.tile_size.x
        y = self.frame.size.y / self.tile_factory.tile_size.y
        return Vector(x, y)

    def pos_in_pixels(self, pos):
        """Returns the position in pixels (x,y) of the given tile pos."""
        return (pos - self.map_pos) * self.tile_factory.tile_size.x

    def is_visible(self, pos):
        """
        Checks if the referenced position is in the visible part of the screen.
        Returns boolean.
        """
        if pos.x >= self.map_pos.x \
           and pos.y >= self.map_pos.y \
           and pos.x <= self.map_pos.x + self.win_size.x \
           and pos.y <= self.map_pos.y + self.win_size.y:
            return True

    def check_position(self, pos):
        """Checks if the given position is on the map."""
        if 0 <= pos.x < self.size.x and \
           0 <= pos.y < self.size.y:
            return True

    def at(self, pos):
        """Returns the symbol of the tile at the given position."""
        if self.check_position(pos):
            return self.map[pos.x][pos.y]

    def check_move(self, vector):
        """
        Checks if the visible part of the map can be moved by
        the given numpy 2D vector.
        """
        newpos = self.map_pos + vector
        if 0 <= newpos.x <= self.size.x - self.win_size.x and \
           0 <= newpos.y <= self.size.y - self.win_size.y:
            return True

    def zoom_to(self, pos):
        """
        Sets the position of the map that the window should zoom in on.
        pos (x,y) are integer indices on the tile map.
        """
        self.map_pos = pos
        self.offset = pos * self.tile_factory.tile_size.x

    def __str__(self):
        return self.get_map()

    def get_map(self):
        rows = '\n'.join(''.join(row) for row in zip(*self.map))
        return rows

    def set_map(self, data):
        """Creates a 2D map with tiles from a multiline string."""
        rows = data.replace('\r', '').strip().split('\n')
        self.fill_map(len(rows[0]), len(rows), '.')
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.map[x][y] = rows[y][x]
        self.cache_map()

    def fill_map(self, xsize, ysize, char):
        """Creates an empty map."""
        self.size = Vector(xsize, ysize)
        self.map = [[char for y in range(ysize)] for x in range(xsize)]

    def draw(self):
        """Draws the map."""
        src = pygame.Rect(self.offset.x, self.offset.y,
                self.win_size_px.x, self.win_size_px.y)
        dest = pygame.Rect(0, 0,
                self.win_size_px.x, self.win_size_px.y)
        self.frame.blit(self.mapsurf, dest, src)

    def get_tile(self, pos):
        return self.tile_factory.get(self.at(pos))

    def set_tile(self, pos, tilename):
        self.map[pos.x][pos.y] = tilename

    def cache_map(self):
        """Creates a static bitmap for a 2D map that is faster."""
        self.mapsurf = pygame.Surface(tuple(self.map_size_px))
        for x in range(self.size.x):
            for y in range(self.size.y):
                tile = self.get_tile(Vector(x, y))
                pos = Vector(tile.size.x * x, tile.size.y * y)
                tile.draw(self.mapsurf, pos)
