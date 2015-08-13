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
from pygame.rect import Rect #numpy import array

class Screen:
    """Manages a display."""
    def __init__(self, resolution, background_image):
        """
        resolution - size of the display in pixels (x,y)
        tile_size - size of tiles in pixels (x,y)
        """
        self.resolution = resolution
        self.rect = Rect(0, 0, resolution.x, resolution.y)
        self.display = pygame.display.set_mode(tuple(resolution))
        self.display = pygame.display.get_surface()
        self.background = pygame.image.load(background_image).convert()
        
    def blit(self, bitmap, destrect, sourcerect):
        """Draws something from the given bitmap on the screen."""
        self.display.blit(bitmap, destrect, sourcerect)

    def clear(self):
        """Wipes out everything."""
        if self.background:
            self.blit(self.background, self.rect, self.rect)
