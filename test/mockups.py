#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

from pygame.event import Event
from pygame.locals import QUIT

from tilegamelib.events import EventGenerator, EventListener
from tilegamelib.game_engine import GameFactory


class MockGenerator(EventGenerator):
    def __init__(self,settings):
        EventGenerator.__init__(self,settings)
        self.queue = []

    def get_events(self):
        while len(self.queue):
            event = self.queue.pop(0)
            print event
            yield event
        quit = Event(QUIT,{})
        print quit
        yield quit

class MockListener(EventListener):
    """EventListener recording key commands."""
    def __init__(self, commandable):
        EventListener.__init__(self, commandable)

    def is_active(self):
        """Event loop has to be activated explicitly to avoid endless loop."""
        return True


class MockGameFactory(GameFactory):

    def create_event_generator(self):
        self.events = MockGenerator(self.settings)
        print self.events
        return self.events
