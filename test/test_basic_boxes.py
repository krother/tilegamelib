#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

from tilegamelib.screen import Frame
from tilegamelib.basic_boxes import TextBox, ImageBox, DictBox
from test_settings import showdoc, TEST_GAME_CONTEXT
from unittest import TestCase, main
import pygame


class BasicBoxTests(TestCase):

    def setUp(self):
        self.frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,160))

    @showdoc
    def test_text_box(self):
        """Display hello world text box."""
        tb = TextBox(self.frame, "Hello World")
        tb.draw()
        pygame.display.update()

    @showdoc
    def test_image_box(self):
        """Display image with colorful boxes."""
        ib = ImageBox(self.frame, "test_data/boxes.png")
        ib.draw()
        pygame.display.update()

    @showdoc
    def test_dict_box(self):
        """Display data from a dictionary."""
        dict_data = {
            'Level':'20',
            'Name':'Zeratul',
            'HP':'400'
            }
        db = DictBox(self.frame, dict_data)
        db.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
