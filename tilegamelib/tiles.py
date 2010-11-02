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

class NoTileError(Exception): pass

class Tile:
    """A tile is a quadratic piece of graphic that can be written
    anywhere on the screen. 
    """
    def __init__(self, name, index, size, image):
        """
        Creates a new tile:
            name  - string identifier
            index - location in rows/columns on the image
            size  - x/y size of the tile
            image - bitmap where the tile is copied from.
        """
        self.name = name
        self.size = size
        self.image = image
        self.box = pygame.Rect(index[0]*size[0],\
                               index[1]*size[1],\
                               size[0],size[1]
                               )
    def __repr__(self):
        return "[Tile '%s' (%ix%i)]"%(self.name,self.size[0],self.size[1])

    def draw(self, frame, pos):
        """Draws the tile on the given position into the bitmap."""
        destrect = pygame.Rect(pos[0],pos[1],
                               self.size[0],self.size[1])
        frame.blit(self.image, destrect, self.box)

    #TODO: check unused
    @property
    def empty_rect(self):
        return pygame.Rect(0,0, self.size[0],self.size[1])

class TileFactory(dict):
    """
    Manages a set of tiles.
    """
    def __init__(self, settings):
        dict.__init__(self)
        self.settings = settings
        self.tile_size = settings.TILE_SIZE
        for xpm_file, spec_file in self.settings.TILE_SETS:
            self.load_tiles(xpm_file, spec_file)
        self.add_tile_synonyms(self.settings.TILE_SYNONYMS)
    

    def get(self,key):
        result = dict.get(self,key,None)
        if not result:
            raise NoTileError("No such tile: %s"%str(key))
        return result

    def load_tiles(self,png_filename,spec_filename):
        """
        Loads tile descriptions from a .spec file, and the tiles from a
        .ong graphics file.
        """
        img = pygame.image.load(png_filename).convert()
        for line in open(spec_filename):
            if line.startswith('#'): continue
            tokens = line.strip().split('\t')
            if len(tokens) == 3:
                xpos, ypos, name = tokens
                # parse where in the img the tiles are
                index = array([int(xpos),int(ypos)])
                self[name] = Tile(name,index,self.tile_size,img)

    def add_tile_synonyms(self,synlist):
        """Processes list of tuples (abbreviation, tile_name)"""
        for abbrev, name in synlist:
            self[abbrev] = self.get(name)
