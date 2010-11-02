#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from tilegamelib.interfaces import Updateable, Commandable
from tilegamelib.screen import Screen
from tilegamelib.events import EventGenerator
from test_settings import TestSettings
from unittest import TestCase, main
from pygame.event import Event
from pygame.locals import KEYDOWN
from mockups import MockGenerator, MockListener
    
class EventTests(TestCase, Updateable, Commandable):
    
    def setUp(self):
        self.updated = 0
        self.result = ""

    def handle_command(self, command):
        self.result += command

    def update(self):
        self.updated += 1

    def test_event_generator(self):
        events = [
            Event(KEYDOWN,{'key':'a'}),
            Event(KEYDOWN,{'key':'c'}),
            Event(KEYDOWN,{'key':'b'}),
        ]
        screen = Screen(TestSettings)
        egen = MockGenerator(TestSettings)
        elis = MockListener(self)
        moves = {
            'a':'Hel',
            'b':'lo',
            'c':'World',
            'd':' '
            }
        elis.set_command_map(moves)
        egen.add_listener(elis)
        egen.queue = events
        egen.event_loop()
        self.assertEqual(self.result, "HelWorldlo")

    def test_events(self):
        screen = Screen(TestSettings)
        egen = EventGenerator(TestSettings)
        egen.add_updateable(self)
        elis = MockListener(self)
        egen.add_listener(elis)
        moves = {
            'a':'Hel',
            'b':'lo',
            'c':'World',
            'd':' '
            }
        elis.set_command_map(moves)
        egen.handle_scripted_keys(list("abdc"))
        self.assertEqual(self.result, "Hello World")
        self.assertEqual(self.updated, 4)


if __name__ == "__main__":
    main()
