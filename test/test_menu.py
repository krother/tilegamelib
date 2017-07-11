#!/usr/bin/env python

import time

import pygame
from pygame import Rect
from pygame.event import Event
from pygame.locals import KEYDOWN

from tilegamelib.config import config
from tilegamelib.events import QUIT_EVENT, EventGenerator
from tilegamelib.frame import Frame
from tilegamelib.menu import VERTICAL_MOVES, MenuBox, TextMenuBox, TileMenuBox
from util import TEST_GAME_CONTEXT, showdoc


class MenuTests:

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
        time.sleep(config.SHORT_DELAY)

    def run_menu(self, menu):
        """Execute some standard operations on the menu and display them."""
        self.draw_menu(menu)
        time.sleep(config.DELAY)
        menu.next_item()
        self.draw_menu(menu)
        menu.next_item()
        self.draw_menu(menu)
        menu.next_item()
        self.draw_menu(menu)
        menu.prev_item()
        self.draw_menu(menu)
        time.sleep(config.DELAY)


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
            Event(KEYDOWN, {'key': 276}),
            Event(KEYDOWN, {'key': 273}),
            Event(KEYDOWN, {'key': 273}),
            Event(KEYDOWN, {'key': 274}),
            Event(KEYDOWN, {'key': 274}),
            Event(KEYDOWN, {'key': 273}),
            Event(KEYDOWN, {'key': 13}),
            Event(KEYDOWN, {'key': 274}),
            QUIT_EVENT,
        ]
        for evt in events:
            self.egen.add_scripted_event(evt)
        MenuBox(self.frame, self.menu, self.egen, VERTICAL_MOVES)
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
        menu = TileMenuBox(factory, self.frame, self.menu,
            self.egen, VERTICAL_MOVES, horizontal=False)
        self.run_menu(menu)

    def test_deactivate_menu(self):
        factory = TEST_GAME_CONTEXT.tile_factory
        menu = TileMenuBox(factory, self.frame, self.menu,
            self.egen, VERTICAL_MOVES, horizontal=False)
        self.assertEqual(len(self.egen.listeners), 1)
        menu.deactivate()
        self.assertEqual(len(self.egen.listeners), 0)
