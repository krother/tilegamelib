#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from basic_boxes import ImageBox, TextBox
from events import EventGenerator
from event_listener import AnyKeyListener
import pygame


class GamePausedBox:
    """Displays a pause box."""

    def __init__(self, frame, image=None, text="Game Paused - press any key to continue", egen=None):
        """Initializes the Pause Box."""
        self.image = ImageBox(frame, image)
        self.text = TextBox(frame, text)
        if egen == None:
            egen = EventGenerator()
        self.egen = egen
        self.elis = AnyKeyListener(self.pause_ended)
        self.egen.add_listener(self.elis)

    def pause_ended(self):
        """Pause ended."""
        self.egen.remove_listener(self.elis)
        
    def draw(self):
        """Draws the Pause Box."""
        self.image.draw()
        self.text.draw()

    def activate(self):
        self.draw()
        pygame.display.update()
        self.egen.event_loop()

