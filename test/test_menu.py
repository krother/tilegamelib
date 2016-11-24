#!/usr/bin/env python

from tilegamelib.frame import Frame
from tilegamelib.menu import MenuBox, TextMenuBox, TileMenuBox, VERTICAL_MOVES
from tilegamelib.events import EventGenerator, QUIT_EVENT
from util import showdoc, DELAY, SHORT_DELAY, TEST_GAME_CONTEXT
from unittest import TestCase, main
from pygame import Rect
from pygame.event import Event
from pygame.locals import KEYDOWN
import pygame
import time


class MenuTests(TestCase):

    def setUp(self):
        self.result = None
        self.frame = Frame(TEST_GAME_CONTEXT.screen, Rect(100, 100, 260, 260))
        self.egen = EventGenerator()

    def select_one(self):
        self.result = 'one'

    def select_two(self):
        self.result = 'two'

    def select_three(self):
        self.result = 'three'

    def draw_menu(self, menu):
        menu.draw()
        pygame.display.update()
        time.sleep(SHORT_DELAY)

    def run_menu(self, menu):
        """Execute some standard operations on the menu and display them."""
        self.draw_menu(menu)
        time.sleep(DELAY)
        menu.next_item()
        self.draw_menu(menu)
        menu.next_item()
        self.draw_menu(menu)
        menu.next_item()
        self.draw_menu(menu)
        menu.prev_item()
        self.draw_menu(menu)
        time.sleep(DELAY)


class TextMenuTests(MenuTests):

    def setUp(self):
        MenuTests.setUp(self)
        self.menu = [
           ('first', self.select_one),
           ('second', self.select_two),
           ('third', self.select_three),
        ]

    def test_menu(self):
        """menu mechanics work."""
        events = [
            Event(KEYDOWN,{'key':276}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':274}),
            Event(KEYDOWN,{'key':273}),
            Event(KEYDOWN,{'key':13}),
            Event(KEYDOWN,{'key':274}),
            QUIT_EVENT,
        ]
        for evt in events:
            self.egen.add_scripted_event(evt)
        menu = MenuBox(self.frame, self.menu, self.egen, VERTICAL_MOVES)
        self.assertEqual(len(self.egen.listeners), 1)
        self.assertEqual(self.result, None)
        self.egen.event_loop()
        self.assertEqual(self.result, 'three')

    @showdoc
    def test_text_menu(self):
        """Displays a text menu plus navigation."""
        menu = TextMenuBox(self.frame, self.menu, self.egen, VERTICAL_MOVES)
        self.run_menu(menu)


class TileMenuTests(MenuTests):

    def setUp(self):
        MenuTests.setUp(self)
        self.menu = [
           ('#', self.select_one),
           ('*', self.select_two),
           ('.', self.select_three),
           ]
        
    @showdoc
    def test_tile_menu(self):
        """Displays a vertical tile menu plus navigation."""
        factory = TEST_GAME_CONTEXT.tile_factory
        menu = TileMenuBox(factory, self.frame, self.menu, self.egen, VERTICAL_MOVES, horizontal=False)
        self.run_menu(menu)

    def test_deactivate_menu(self):
        factory = TEST_GAME_CONTEXT.tile_factory
        menu = TileMenuBox(factory, self.frame, self.menu, self.egen, VERTICAL_MOVES, horizontal=False)
        self.assertEqual(len(self.egen.listeners),1)
        menu.deactivate()
        self.assertEqual(len(self.egen.listeners),0)



if __name__ == "__main__":
    main()
