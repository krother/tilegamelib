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
from tilegamelib.menu import MenuBox, TextMenuBox, TileMenuBox
from test_settings import TestSettings,showdoc,DELAY,SHORT_DELAY, TEST_GAME_CONTEXT
from unittest import TestCase, main
from test_events import MockGenerator
from pygame.event import Event
from pygame.locals import KEYDOWN
import pygame
import time

MENU = [
   ('first',"1"),
   ('second',"2"),
   ('third',"3"),
    ]
TILE_MENU = [
   ('r',"1"),
   ('g',"2"),
   ('b',"3"),
    ]

class MenuTests(TestCase):

    @showdoc
    def test_menu(self):
        """menu mechanics work."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,260))
        egen = MockGenerator(TestSettings)
        egen.queue =  [
            Event(KEYDOWN,{'key':276}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':13}),
            Event(KEYDOWN,{'key':274}),
            ]
        mp = MenuBox(frame, MENU, egen=egen, moves=frame.settings.MENU_MOVES, horizontal=False)
        self.assertEqual(len(egen.listeners),1)
        self.assertEqual(mp.result,None)
        egen.event_loop()
        self.assertEqual(mp.result,'3')

    @showdoc
    def test_text_menu(self):
        """Displays a text menu and selecting from it."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,260))
        egen = MockGenerator(TestSettings)
        mp = TextMenuBox(frame, MENU, egen=egen, moves=frame.settings.MENU_MOVES, horizontal=False)
        self.run_menu(mp)

    @showdoc
    def test_tile_menu(self):
        """Displays a vertical tile menu and selecting from it."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,260))
        egen = MockGenerator(TestSettings)
        mp = TileMenuBox(TEST_GAME_CONTEXT.tile_factory, frame, TILE_MENU, egen=egen, moves=frame.settings.MENU_MOVES, horizontal=False)
        self.run_menu(mp)

    def run_menu(self, mp):
        mp.draw()
        pygame.display.update()
        time.sleep(DELAY)
        mp.choose_next()
        mp.draw()
        pygame.display.update()
        time.sleep(SHORT_DELAY)
        mp.choose_next()
        mp.draw()
        pygame.display.update()
        time.sleep(SHORT_DELAY)
        mp.choose_next()
        mp.draw()
        pygame.display.update()
        time.sleep(SHORT_DELAY)
        mp.choose_previous()
        mp.draw()
        pygame.display.update()



if __name__ == "__main__":
    main()
