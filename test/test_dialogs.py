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
from tilegamelib.highscores import HighscoreBox
from tilegamelib.game_paused import GamePausedBox
from tilegamelib.game_over import GameOverBox
from test_settings import TestSettings, showdoc, HIGHSCORE_BACKUP, TEST_GAME_CONTEXT
from test_events import MockGenerator
import pygame
from pygame.event import Event
from pygame.locals import KEYDOWN
from unittest import TestCase, main


class GameOverTests(TestCase):

    @showdoc
    def test_game_over(self):
        """Display box with Game Over message for a while."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,160))
        go = GameOverBox(TEST_GAME_CONTEXT, frame)
        go.activate()

class GamePausedTests(TestCase):

    @showdoc
    def test_game_paused(self):
        """Display pause box."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,160))
        egen = MockGenerator(TestSettings)
        egen.queue =  [Event(KEYDOWN,{'key':'a'})]
        gp = GamePausedBox(TEST_GAME_CONTEXT, frame, egen=egen)
        gp.draw()
        pygame.display.update()
        elis = egen.listeners[0]
        self.assertTrue(elis.paused)
        gp.activate()
        self.assertFalse(elis.paused)


class HighscoreTests(TestCase):

    def setUp(self):
        scores = open(HIGHSCORE_BACKUP).read()
        open(TestSettings.HIGHSCORE_FILE,'w').write(scores)

    @showdoc
    def test_highscores(self):
        """Display highscore list."""
        frame = Frame(TEST_GAME_CONTEXT, (100,20), (260,360))
        egen = MockGenerator(TestSettings)
        egen.queue =  [
            Event(KEYDOWN,{'key':65}),
        ]
        hsc = HighscoreBox(TEST_GAME_CONTEXT, frame, egen)
        hsc.activate()

    @showdoc
    def test_add_score(self):
        """BOBO is added to high score list."""
        frame = Frame(TEST_GAME_CONTEXT, (100,20), (260,360))
        egen = MockGenerator(TestSettings)
        egen.queue =  [
            Event(KEYDOWN,{'key':66}),
            Event(KEYDOWN,{'key':79}),
            Event(KEYDOWN,{'key':66}),
            Event(KEYDOWN,{'key':79}),
            Event(KEYDOWN,{'key':13}),
            Event(KEYDOWN,{'key':13}),
        ]
        hsc = HighscoreBox(TEST_GAME_CONTEXT, frame, egen)
        hsc.enter_score(999999)
        hsc.activate()
        self.assertEqual(hsc.highscores.scores[0],(999999,'BOBO'))

if __name__ == "__main__":
    main()
