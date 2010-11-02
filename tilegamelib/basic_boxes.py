#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


"""
Controllers for dialog functions.
"""

from interfaces import Drawable
import numpy as np
import pygame

class TextBox(Drawable):
    """Displays a box with text."""
    def __init__(self, frame, text, x_offset=0, y_offset=0, font=None, color=None):
        """Initializes the TextBox."""
        self.frame = frame
        self.text = text
        self.font = font
        self.color = color
        self.pos = np.array([x_offset,y_offset])

    def draw(self):
        """Draws the Box."""
        self.frame.clear()
        self.frame.print_text(self.text, self.pos, self.font, self.color)


class ImageBox(Drawable):
    """
    Displays a box with an image.
    """
    def __init__(self, frame, image_fn=None):
        """Initializes the ImageBox."""
        self.frame = frame
        self.image = pygame.image.load(image_fn).convert()

    def draw(self):
        """Draws the Box."""
        self.frame.clear()
        self.frame.blit(self.image, self.frame.box, \
            pygame.Rect(0,0,self.frame.size[0],self.frame.size[1]))


class DictBox(Drawable):
    """
    Text window displaying scores etc. taken from a data dictionary
    """    
    def __init__(self, frame, data, labels=None):
        self.frame = frame
        self.data = data
        self.labels = labels

    def draw(self):
        """Draws some values from the dictionary."""
        self.frame.clear()
        if self.labels:
            labels = self.labels
        else:
            labels = self.data.keys()
            labels.sort()
        for i,lab in enumerate(labels):
            pos = np.array([50, 50+20*i])
            self.frame.print_text('%s : %s'%(lab, str(self.data[lab])),pos)

class FpsBox(TextBox):
    """Displays FPS rate"""    
    def __init__(self,screen,pos):
        super.__init__(self,screen,pos,array(50,20))
        self.fps = 0.0
        self.lasttime = time.time()

    def update(self):
        """
        Measures the time passed since the last call
        and calculates the FPS rate (frames per second).
        """
        now = time.time()
        diff = now-self.lasttime
        self.lasttime = now
        if diff>0:
            self['fps'] = 1.0/diff

    def draw(self):
        """Draws some values from the dictionary."""
        self.clear()
        self.print_text('%3.1f fps'%self['fps'],self.font,BLUE,self.pos+20)
        
