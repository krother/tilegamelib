#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


import sys
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, QUIT

"""
Observer pattern for event handling:

EventGenerator - creates event objects

EventListener - handles event objects (abstract class)

"""

class EventGenerator:
    """
    Class that provides an event loop.
    In the loop, key and mouse events are dispatched
    to EventListeners that are registered to it.
    """
    def __init__(self, settings):
        self.settings = settings
        self.lastkey = 0
        self.key_repeat_delay = settings.DEFAULT_KEY_REPEAT
        self.last_mouse_event = None
        self.delay = 1
        self.listeners = []
        self.updateables = []
        self._key_queue = []
        
    def add_listener(self,listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self,listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def mousebutton_pressed(self,event):
        """Called each time a mouse button is pressed."""
        if event.button == 1:
            for l in self.listeners: l.leftclick(event.pos)
        elif event.button == 3:
            for l in self.listeners: l.rightclick(event.pos)
    
    def mousebutton_released(self, event):
        """Called each time a mouse button is released."""
        pass

    def key_pressed(self, event):
        """
        Called each time a key is pressed down.
        Calls handle_key in regular intervals.
        """
        self.lastkey = event.key
        self.key_repeat_delay = self.settings.KEY_REPEAT.get(self.lastkey, self.settings.DEFAULT_KEY_REPEAT)
        for l in self.listeners:
            l.handle_key(event.key)

    def key_released(self,event):
        """Called each time a key is released."""
        self.lastkey = 0

    def exit_signalled(self, event):
        """Takes care of Ctrl-C and other interrupting struff."""
        sys.stderr.write('event loop terminated by QUIT signal.\n')
        self.listeners = []

    event_handlers = {
        MOUSEBUTTONDOWN: mousebutton_pressed,
        MOUSEBUTTONUP: mousebutton_released,
        KEYDOWN: key_pressed,
        KEYUP: key_released,
        QUIT: exit_signalled
        }

    def get_events(self):
        pygame.event.pump()
        return pygame.event.get()
    
    def handle_events(self):        
        """Gets events resulting from user actions and identifies them."""
        for event in self.get_events():
            handler = self.event_handlers.get(event.type,None)
            if handler:
                handler(self,event)
        # make key repeats
        if self.lastkey and self.key_repeat_delay > 0:
            self.key_repeat_delay -= 1
            if self.key_repeat_delay == 0:
                self.key_repeat_delay = self.settings.KEY_REPEAT.get(self.lastkey, self.settings.DEFAULT_KEY_REPEAT)
                for l in self.listeners:
                    l.handle_key(self.lastkey)

    def handle_scripted_keys(self,keys):
        """Implemented for testing. Handles a list of key events."""
        # no delay here
        while keys:
            key = keys.pop(0)
            for l in self.listeners:
                l.handle_key(key)
            self.call_update()

    def is_running(self):
        """One running listener is enough."""
        for l in self.listeners:
            if l.is_active():
                return True


    def event_loop(self):
        """
        Processes events, updates and draws the instance
        until is_event_loop_running returns False.
        """
        while self.is_running():
            if self._key_queue != []:
                self.handle_scripted_keys(self.key_queue)
            self.handle_events()
            self.call_update()
            pygame.time.delay(self.delay)

    def add_updateable(self, up):
        self.updateables.append(up)

    def remove_updateable(self, up):
        if up in self.updateables:
            self.updateables.remove(up)

    def call_update(self):
        """Calls update() of an updateable in regular intervals."""
        for up in self.updateables:
            up.update()




class EventListener:
    """
    Abstract class for handling events.
    """
    def __init__(self, commandable=None):
        self.command_map = {}
        self.commandable = commandable
        
    def leftclick(self,pos):
        """Called each time the left mouse button is clicked."""
        pass

    def rightclick(self,pos):
        """Called each time the right mouse button is clicked."""
        pass

    def set_command_map(self, cmdmap):
        self.command_map = cmdmap
        
    def handle_key(self,key):
        """Called each time a key event needs to be handled."""
        cmd = self.command_map.get(key)
        if cmd and self.commandable:
            self.commandable.handle_command(cmd)

    def rename_command(self, old, new):
        """Changes values of command dict."""
        for key in self.command_map:
            if self.command_map[key] == old:
                self.command_map[key] = new
                return
                                
    def is_active(self):
        """Controls when the event loop should be terminated. Returns boolean."""
        return False
    
    
