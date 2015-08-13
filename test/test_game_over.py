#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from tilegamelib.frame import Frame
from tilegamelib.game_over import GameOverBox
from test_settings import TestSettings, showdoc, BOX_IMAGE, TEST_GAME_CONTEXT, DEMIBOLD_BIG, WHITE
import pygame
from pygame import Rect
from unittest import TestCase, main


class GameOverTests(TestCase):

    @showdoc
    def test_game_over(self):
        """Display box with Game Over message."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100,100, 260,160))
        go = GameOverBox(frame, BOX_IMAGE, font=DEMIBOLD_BIG, color=WHITE)
        go.activate()


if __name__ == "__main__":
    main()
