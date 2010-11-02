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
from screen import GameElement
import pygame

class GameOverBox(Drawable, Modal, GameElement):
    """Displays a game over box."""

    def __init__(self, context, frame, text="Game Over", image_fn=None):
        """Initializes the Game Over Box."""
        GameElement.__init__(self, context)
        self.delay = frame.settings.GAME_OVER_DELAY
        self.image = None
        if image_fn:
            self.image = ImageBox(frame, image_fn)
        offset = self.settings.GAME_OVER_OFFSET
        self.text = TextBox(frame, text, offset[0], offset[1], \
            self.settings.DEMIBOLD_BIG, color=self.settings.WHITE)

    def play_sound(self):
        snd_name = self.settings.GAME_OVER_SOUND.get(self.text)
        if snd_name:
            self.play_effect(snd_name)

    def draw(self):
        if self.image:
            self.image.draw()
        self.text.draw()

    def activate(self):
        self.draw()
        self.play_sound()
        pygame.display.update()
        pygame.time.delay(self.delay)



