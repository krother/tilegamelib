#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


import pygame
from pygame.locals import *
from numpy import array
from tilegamelib.interfaces import Drawable, Updateable
from sprites import Sprite, SpriteList
from screen import GameElement

class Move:
    """
    instruction to move a tile.
    """
    def __init__(self, pos, tile, vector, steps=1, speed=1):
        self.pos = pos
        self.vector = vector
        self.tile = tile
        self.steps = steps
        self.speed = speed

    def __eq__(self, other):
        if self.pos == other.pos \
            and self.tile == other.tile \
            and str(self.vector) == str(other.vector) \
            and self.steps == other.steps \
            and self.speed == other.speed:
                return True


class TiledMap(Drawable, GameElement):
    """
    Abstract class that supports drawing of a map
    consisting of 2D-tiles. The map can be scrolled
    in a way that only a part of the map is displayed.
    """
    def __init__(self, context, frame):
        """
        Class for displaying a static map of tiles
        (a background, landscape etc.) that does not change.

        frame - Frame object
        """
        GameElement.__init__(self, context)
        self.frame = frame
        # position variables    
        self.offset = array([0,0])
        self.map_pos = array([0,0])        
        self.map_size = array([0,0])        
        self.map = []
        self.mapsurf = None
        
    @property
    def win_size_px(self):
        """size of the map window in pixels (x,y)."""
        return self.win_size * self.tile_factory.tile_size

    @property
    def map_size_px(self):
        """size of the map in pixels (x,y)."""
        return self.map_size * self.tile_factory.tile_size
    
    @property
    def win_size(self):
        """size of the window in tiles."""
        x = self.frame.size[0]/self.tile_factory.tile_size[0]
        y = self.frame.size[1]/self.tile_factory.tile_size[1]
        return array([x,y])

    def set_map_size(self,map_size):
        self.map_size = map_size

    def pos_in_pixels(self,pos):
        """
        Returns the position in pixels (x,y) of the given tile pos.
        """
        return (pos-self.map_pos)* self.factory.tile_size

    def is_visible(self, pos):
        """
        Checks if the referenced position is in the visible part of the screen.
        Returns boolean.
        """
        if pos[0] >= self.map_pos[0] \
           and pos[1] >= self.map_pos[1] \
           and pos[0] <= self.map_pos[0]+self.win_size[0] \
           and pos[1] <= self.map_pos[1]+self.win_size[1]:
               return True

    def check_position(self, pos):
        """Checks if the given position is on the map."""
        if 0 <= pos[0] < self.map_size[0] and\
           0 <= pos[1] < self.map_size[1]:
            return True

    def check_move(self, vector):
        """
        Checks if the visible part of the map can be moved by
        the given numpy 2D vector.
        """
        newpos = self.map_pos + vector
        if 0 <= newpos[0] <= self.map_size[0]-self.win_size[0] and\
           0 <= newpos[1] <= self.map_size[1]-self.win_size[1]:
            return True

    def zoom_to(self, pos):
        """
        Sets the position of the map that the window should zoom in on.
        pos (x,y) are integer indices on the tile map.
        """
        self.map_pos = pos
        self.offset = pos*self.tile_factory.tile_size

    def __str__(self):
        return str(self.map)
    
    def load_map(self,map_filename):
        """
        Reads a map from an ascii file encoded
        on a one character - one tile base.
        """
        data = open(map_filename,'r').read()
        self.fill_map(data)

    def fill_map(self,data):
        """Creates a 2D map with tiles from a multiline string."""
        lines = data.split('\n')
        self.create_empty_map(lines)
        self.parse_map(lines)
        self.cache_map()

    def create_empty_map(self, lines):
        """Creates an empty map array of aproppriate size."""
        xsize = len(lines[0])
        ysize = len(lines)
        self.set_map_size(array([xsize,ysize]))
        self.map = [['.' for y in range(ysize)] for x in range(xsize)]

    def parse_map(self, lines):
        """
        Parses lines of 2D tiles on a one character - one tile base.
        Results in self.map being a 2D array of characters.
        """
        self.create_empty_map(lines)
        for y,line in enumerate(lines):
            for x,char in enumerate(line):
                self.map[x][y] = char


    def draw(self):
        """Draws the map."""
        rect = pygame.Rect(self.offset[0],self.offset[1],\
                                 self.win_size_px[0],self.win_size_px[1])
        self.frame.blit(self.mapsurf, rect, rect)

    def get_tile(self, pos):
        return self.tile_factory.get(self.map[pos[0]][pos[1]])

    def set_tile(self, pos, tile):
        self.map[pos[0]][pos[1]] = tile

    def cache_map(self):
        """
        Creates a static bitmap for a 2D map that is even faster.
        """
        self.mapsurf = pygame.Surface(self.map_size_px)
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                tile = self.get_tile((x,y))
                pos = array([tile.size[0]*x,tile.size[1]*y])
                tile.draw(self.mapsurf,pos)
                

class MoveableTiledMap(TiledMap, Updateable):
    """
    map that allows to move tiles.
    """
    def __init__(self, context, frame):
        TiledMap.__init__(self, context, frame)
        self.sprites = SpriteList()

    def draw(self):
        TiledMap.draw(self)
        self.sprites.draw()

    def are_tiles_moving(self):
        return self.sprites.is_moving()
    
    def update(self):
        self.sprites.update()
        #if len(self.sprites)>0 and not self.are_tiles_moving():
        self.cleanup()

    def move_tile(self, move):
        """Starts the moving of a map tile."""
        tile = self.get_tile(move.pos)
        sprite = Sprite(self.frame, tile, move.pos, speed=move.speed)
        self.sprites.append(sprite)
        self.map[move.pos[0]][move.pos[1]] = '.'
        newpos = move.pos
        for s in range(move.steps):
            newpos = newpos + move.vector
            if self.check_position(newpos):
                sprite.add_move(move.vector)
        self.cache_map()

    def cleanup(self):
        """removes sprites not needed."""
        sprites = [s for s in self.sprites]
        for s in sprites:
            if not s.is_moving():
                self.sprites.remove(s)
                self.map[s.pos[0]][s.pos[1]] = s.tile.name
        self.cache_map()

    #TODO: Check easter eggs
    def random_move(self):
        """Adds a random move to the movement queue."""
        r = int(random()*len(self.settings.MOVES.values()))
        for j in range(int(random()*10)):
            self.path.append(self.settings.MOVES.values()[r])


        



