#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from interfaces import Drawable, Updateable
from random import random
from numpy import array
import pygame
from pygame.locals import *


class Sprite(Drawable):
    """
    Object that moves along a tile grid. Sprites have a queue of moves.
    """
    def __init__(self, frame, tile, pos=None, speed=1):
        """
        frame - Frame object
        tilemap - TiledSpriteMap object
        pos - position in tiles as a numpy array (x,y)
        tile - tile that the sprite shows.
        """
        self.frame = frame
        self.tile = tile
        self.size = self.tile.size
        self.pos = pos # position in tiles
        if pos == None:
            self.pos = array([0,0])
        
        # sprite movement
        self.path = [] # Queue of moves
        self.move_offset = array([0,0]) # offset on position in pixels
        self.move_count = 0
        self.speed = speed

    def add_move(self,move):
        """Adds a move to the movement queue."""
        self.path.append(move)

    def add_priority_move(self,move):
        """Adds a move to first position of the movement queue."""
        self.path = [move] + self.path

    def is_moving(self):
        if self.path or self.move_count:
            return True

    def is_visible(self):
        return True
                        
    def move(self):
        """apply path to object vector and perform movement."""
        if self.move_count <= 0:
            if len(self.path)>0:
                self.vector = self.path.pop(0)
                self.move_count = self.size[0]
                    
        # perform movement
        if self.move_count > 0:
            self.move_offset = self.vector*(self.size[0]-self.move_count)
            self.move_count -= self.speed
            if self.move_count <= 0:
                # objective reached
                self.pos += self.vector
                self.move_offset = array([0,0])

    def draw(self):
        """
        Draw the sprite on the screen (if it is inside bounds).
        """
        if self.is_visible():
            pos = self.pos*self.size + self.move_offset
            destrect = pygame.Rect(pos[0],pos[1],\
                                   self.size[0],self.size[1]
                                   )
            self.tile.draw(self.frame, destrect)




class AnimationSequence(Drawable, Updateable):
    """
    Class looping through a sequence of tiles.
    """
    def __init__(self, frame, tile_seq, pos=None, delay=20):
        self.frame = frame
        self.sequence = tile_seq
        self.phase = 0
        self.pos = pos
        self.delay = delay
        self.delay_counter = self.delay
        self.sprite = self.create_sprite()
        print self.sprite.pos
        print self.sprite.size

    @property
    def finished(self):
        return self.phase == len(self.sequence)

    def create_sprite(self):
        return Sprite(self.frame, self.sequence[self.phase], self.pos)

    def update(self):
        if self.delay_counter > 0:
            self.delay_counter -= 1
        else:
            self.phase += 1
            if not self.finished:
                # go to next phase & create new sprite
                self.delay_counter = self.delay
                self.sprite = self.create_sprite()

    def draw(self):
        self.sprite.draw()
        
        
class SpriteList(list, Drawable, Updateable):
    """
    Class for displaying a set of movable objects.
    """
    def draw(self):
        for sprite in self:
            sprite.draw()

    def is_moving(self):
        for sprite in self:
            if sprite.is_moving():
                return True

    def update(self):
        for sprite in self:
            sprite.move()
