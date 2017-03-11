#!/usr/bin/env python

from tilegamelib.frame import Frame
from tilegamelib.dialogs.game_paused import GamePausedBox
from tilegamelib.events import EventGenerator
from util import showdoc, TEST_GAME_CONTEXT
from test_data import PAUSE_IMAGE
import pygame
from pygame import Rect
from unittest import TestCase, main


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
