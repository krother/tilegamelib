#!/usr/bin/env python

import time

import pygame
import pytest
from pygame.event import Event
from pygame.locals import KEYDOWN

from tilegamelib.config import config
from tilegamelib.events import QUIT_EVENT, EventGenerator
from tilegamelib.menu import VERTICAL_MOVES, MenuBox, TextMenuBox, TileMenuBox


@pytest.fixture
def event_gen():
    return EventGenerator()


class TestMenu:

    def setup(self):
        self.result = None
        self.callbacks = [self.select_one, self.select_two, self.select_three]

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


class TestTextMenu(TestMenu):

    labels = ['first', 'second', 'third']

    def test_menu(self, frame, event_gen):
        """menu mechanics work."""
        text_menu = list(zip(self.labels, self.callbacks))
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
            event_gen.add_scripted_event(evt)
        MenuBox(frame, text_menu, event_gen, VERTICAL_MOVES)
        assert len(event_gen.listeners) == 1
        assert self.result is None
        event_gen.event_loop()
        assert self.result == 'three'

    def test_text_menu(self, frame, event_gen):
        """Displays a text menu plus navigation."""
        text_menu = list(zip(self.labels, self.callbacks))
        menu = TextMenuBox(frame, text_menu, event_gen, VERTICAL_MOVES)
        self.run_menu(menu)


class TestTileMenu(TestMenu):

    def test_tile_menu(self, frame, event_gen, tile_factory):
        """Displays a vertical tile menu plus navigation."""
        tile_menu = list(zip('#*.', self.callbacks))
        menu = TileMenuBox(
            tile_factory, frame, tile_menu,
            event_gen, VERTICAL_MOVES, horizontal=False)
        self.run_menu(menu)

    def test_deactivate_menu(self, frame, event_gen, tile_factory):
        tile_menu = list(zip('#*.', self.callbacks))
        menu = TileMenuBox(
            tile_factory, frame, tile_menu,
            event_gen, VERTICAL_MOVES, horizontal=False)
        assert len(event_gen.listeners) == 1
        menu.deactivate()
        assert len(event_gen.listeners) == 0
