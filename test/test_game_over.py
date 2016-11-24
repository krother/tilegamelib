#!/usr/bin/env python

from tilegamelib.frame import Frame
from tilegamelib.dialogs.game_over import GameOverBox
from util import showdoc, TEST_GAME_CONTEXT
from test_data import DEMIBOLD_BIG, WHITE, GAME_OVER_IMAGE
from pygame import Rect
from unittest import TestCase, main


class GameOverTests(TestCase):

    @showdoc
    def test_game_over(self):
        """Display box with Game Over message."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 160))
        go = GameOverBox(frame, GAME_OVER_IMAGE, font=DEMIBOLD_BIG, color=WHITE)
        go.activate()


if __name__ == "__main__":
    main()
