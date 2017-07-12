#!/usr/bin/env python

from unittest import TestCase, main

from pygame import Rect

from test.util import TEST_GAME_CONTEXT, showdoc
from tilegamelib.config import config
from tilegamelib.dialogs.game_over import GameOverBox
from tilegamelib.frame import Frame


class GameOverTests(TestCase):

    @showdoc
    def test_game_over(self):
        """Display box with Game Over message."""
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 160))
        go = GameOverBox(frame, config.GAME_OVER_IMAGE,
            font=config.DEMIBOLD_BIG, color=config.WHITE)
        go.activate()

    def dummy(self, filename):
        assert filename == 'bar'


if __name__ == "__main__":
    main()
