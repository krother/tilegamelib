#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

import time
from unittest import main
from unittest import TestCase

from pygame.event import Event
from pygame.locals import KEYDOWN

from mockups import MockGameFactory
from test_settings import DELAY
from test_settings import showdoc
from test_settings import TestSettings
from tilegamelib.game_engine import GameEngine


class GameEngineTests(TestCase):

    def setUp(self):
        self.factory = MockGameFactory(TestSettings)
        self.engine = GameEngine(self.factory)
        self.events = self.factory.events

    @showdoc
    def test_show_menu(self):
        """Displays a main menu."""
        self.events.queue = [
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':13}),
            ]
        result = self.engine.show_menu()
        self.assertEqual(result, 'two player game')

    @showdoc
    def test_show_game_over(self):
        """Displays a game over window."""
        self.engine.show_game_over('Game Over Test')

    @showdoc
    def test_show_highscores(self):
        """Enters something into the highscore list."""
        self.events.queue =  [
            Event(KEYDOWN,{'key':66}),
            Event(KEYDOWN,{'key':67}),
            Event(KEYDOWN,{'key':13}),
            Event(KEYDOWN,{'key':13}),
            ]
        self.engine.show_highscores(333)

    def test_activate(self):
        pass
        #TODO: REMOVE ENDLESS LOOP!
        # self.engine.activate()

if __name__ == "__main__":
    main()
