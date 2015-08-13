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
from tilegamelib.game_paused import GamePausedBox
from tilegamelib.events import EventGenerator, QUIT_EVENT
from test_settings import TestSettings, showdoc, TEST_GAME_CONTEXT, BOX_IMAGE
import pygame
from pygame import Rect
from unittest import TestCase, main


class GamePausedTests(TestCase):

    @showdoc
    def test_game_paused(self):
        """Display pause box."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100,100, 260,160))
        egen = EventGenerator(TestSettings)
        egen.add_scripted_keys(['a'])
        gp = GamePausedBox(frame, BOX_IMAGE, text='test game paused signal', egen=egen)
        gp.draw()
        pygame.display.update()
        gp.activate()


if __name__ == "__main__":
    main()
