#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from interfaces import GameContext
import pygame
from pygame.locals import *
from numpy import array

class Screen:
    """Manages a display."""
    def __init__(self,settings):
        """
        resolution - size of the display in pixels (x,y)
        tile_size - size of tiles in pixels (x,y)
        """
        self.settings = settings
        resolution = settings.RESOLUTION
        self.box = array([0,0,resolution[0],resolution[1]])
        self.display = pygame.display.set_mode(resolution)
        self.display = pygame.display.get_surface()
        self.background = pygame.image.load(settings.BACKGROUND_IMAGE).convert()
                        
    def blit(self, bitmap, destrect, sourcerect):
        """Draws something from the given bitmap on the screen."""
        self.display.blit(bitmap, destrect, sourcerect)

    def clear(self):
        """Wipes out everything."""
        if self.background:
            self.blit(self.background, self.box, self.box)


class GameElement(GameContext):
    def __init__(self, game_context):
        self.context = game_context
        self.settings = game_context.settings
        self.screen = game_context.screen
        self.effects = game_context.effects
        self.music = game_context.music
        self.events = game_context.events
        self.tile_factory = game_context.tile_factory


class Frame(GameElement):
    """Rectangular piece of the screen."""
    def __init__(self, context, pos, size):
        """
        pos - position of the map on the screen in pixels (x,y)
        size - size of the element in pixels (x,y)
        """
        GameElement.__init__(self, context)
        self.box = pygame.Rect(pos[0],pos[1],size[0],size[1])

    @property
    def pos(self):
        return (self.box.x, self.box.y)
    
    @property
    def size(self):
        return self.box.size

    def get_dest_pos(self, pos):
        """Returns position of pos added to own position."""
        xp = self.box.x + pos[0]
        yp = self.box.y + pos[1]
        return xp, yp
        
    def get_dest_rect(self, rect):
        """Returns position of rect added to own position."""
        pos = self.get_dest_pos((rect.x, rect.y))
        return pygame.Rect(pos[0], pos[1], rect.size[0], rect.size[1])
    
    def blit(self, bitmap, rect, sourcerect):
        """Copies graphics on the screen (quick)."""
        destrect = self.get_dest_rect(rect)
        self.screen.blit(bitmap, destrect, sourcerect)

    def print_text(self, text, pos, font=None, color=None):
        """Writes text on the screen."""
        if not font: font = self.settings.DEMIBOLD_BIG
        if not color: color = self.settings.GREEN
        scr = font.render(text,1,color)
        pos = self.get_dest_pos(pos)
        self.screen.display.blit(scr,pos)

    def clear(self):
        """Clears the area within this ScreenElement instance."""
        self.screen.blit(self.screen.background, self.box, pygame.Rect(0,0,self.size[0],self.size[1]))

