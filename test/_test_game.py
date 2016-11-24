#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from unittest import main,TestCase
from tilegamelib.screen import Frame
from test_game_engine import MockGameFactory
from test_settings import TestSettings, showdoc
from test_player import MockPlayer
import pygame

class GameTests(TestCase):

    def setUp(self):
        factory = MockGameFactory(TestSettings)
        factory.create_screen()
        factory.create_event_generator()
        factory.create_tile_factory()
        self.game = factory.create_game('one player game')
        frame = Frame(factory, (100,20), (260,360))
        p = MockPlayer(factory, frame)
        self.game.players.append(p)

    @showdoc
    def test_draw(self):
        """Displays a game instance (colorful map)"""
        self.game.draw()
        pygame.display.update()

    def test_update(self):
        self.game.update()

    def test_terminate(self):
        self.game.terminate()
        self.assertEqual(len(self.game.players),0)

if __name__ == "__main__":
    main()
