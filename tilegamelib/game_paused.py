#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from interfaces import Drawable, Modal
from basic_boxes import ImageBox, TextBox
from events import EventGenerator, EventListener
from screen import GameElement
import pygame

class AnyKeyListener(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.paused = True

    def is_active(self):
        return self.paused

    def handle_key(self,key):
        if key != 27:
            self.paused = False


class GamePausedBox(Drawable, Modal, GameElement):
    """Displays a pause box."""

    def __init__(self, context, frame, text="Game Paused - press any key to continue",egen=None):
        """Initializes the Pause Box."""
        GameElement.__init__(self, context)
        self.image = ImageBox(frame, self.settings.BOX_IMAGE)
        self.text = TextBox(frame, text)
        if egen == None:
            egen = EventGenerator(self.settings)
        self.egen = egen
        elis = AnyKeyListener()
        self.egen.add_listener(elis)

    def draw(self):
        """Draws the Pause Box."""
        self.image.draw()
        self.text.draw()

    def activate(self):
        self.draw()
        pygame.display.update()
        self.egen.event_loop()

