#!/usr/bin/env python

from unittest import main
from unittest import TestCase

from pygame import Rect

from test_data import DEMIBOLD_BIG
from test_data import GAME_OVER_IMAGE
from test_data import WHITE
from tilegamelib.dialogs.game_over import GameOverBox
from tilegamelib.frame import Frame
from util import showdoc
from util import TEST_GAME_CONTEXT


class GameOverTests(TestCase):

    @showdoc
    def test_game_over(self):
        """Display box with Game Over message."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 160))
        go = GameOverBox(frame, GAME_OVER_IMAGE, font=DEMIBOLD_BIG, color=WHITE)
        go.activate()


if __name__ == "__main__":
    main()
