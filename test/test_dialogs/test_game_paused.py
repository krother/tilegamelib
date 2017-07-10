#!/usr/bin/env python

from unittest import main
from unittest import TestCase

import pygame
from pygame import Rect

from test_data import PAUSE_IMAGE
from tilegamelib.dialogs.game_paused import GamePausedBox
from tilegamelib.events import EventGenerator
from tilegamelib.frame import Frame
from util import showdoc
from util import TEST_GAME_CONTEXT


class GamePausedTests(TestCase):

    @showdoc
    def test_game_paused(self):
        """Display pause box."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 160))
        egen = EventGenerator()
        egen.add_scripted_keys(['a'])
        gp = GamePausedBox(frame, PAUSE_IMAGE, text='test game paused signal', egen=egen)
        gp.draw()
        pygame.display.update()
        gp.activate()


if __name__ == "__main__":
    main()
