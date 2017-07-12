
import pygame
from pygame.event import Event
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT


"""
Observer pattern for event handling:
    EventGenerator - creates event objects
    event_listener.EventListener - handles event objects (abstract class)
"""

QUIT_EVENT = Event(QUIT, {})


class EventGenerator:
    """
    Class that provides an event loop.
    In the loop, key and mouse events are dispatched
    to EventListeners that are registered to it.
    """
    def __init__(self, game_delay=10, key_repeat=80):
        self.lastkey = 0
        self.game_delay = game_delay
        self.key_repeat = key_repeat
        self.key_repeat_delay = key_repeat
        self.last_mouse_event = None
        self.listeners = []
        self.callbacks = []
        self.user_events = {}
        self.event_queue = []

    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def cleanup_listeners(self):
        self.listeners = [l for l in self.listeners if not l.terminated]

    def add_callback(self, callback):
        """Adds callback object with an update() method."""
        assert hasattr(callback, 'update')
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def add_scripted_event(self, event):
        self.event_queue.append(event)

    def add_scripted_keys(self, keys, converter=ord):
        """Queues a list of key events."""
        for key in keys:
            event = Event(KEYDOWN, {'key': converter(key)})
            self.event_queue.append(event)

    # -------------- methods taking care of event types ----------
    def mousebutton_pressed(self, event):
        """Called each time a mouse button is pressed."""
        if event.button == 1:
            for l in self.listeners:
                l.leftclick(event.pos)
        elif event.button == 3:
            for l in self.listeners:
                l.rightclick(event.pos)

    def mousebutton_released(self, event):
        """Called each time a mouse button is released."""
        pass

    def key_pressed(self, event):
        """
        Called each time a key is pressed down.
        Makes key repeats
        """
        if self.lastkey == event.key:
            if self.key_repeat_delay > 0:
                self.key_repeat_delay -= 1
            if self.key_repeat_delay == 0:
                self.key_repeat_delay = self.key_repeat
                for l in self.listeners:
                    l.handle_key(self.lastkey)
        else:
            self.key_repeat_delay = self.key_repeat
            for l in self.listeners:
                l.handle_key(event.key)
        self.lastkey = event.key

    def key_released(self, event):
        """Called each time a key is released."""
        self.lastkey = 0

    def exit_signalled(self, event=None):
        """Takes care of Ctrl-C and other interrupting stuff."""
        self.listeners = []

    def get_events(self):
        """Returns a scripted or user-generated event."""
        if self.event_queue:
            return [self.event_queue.pop(0)]
        else:
            pygame.event.pump()
            return pygame.event.get()

    def empty_event_queue(self):
        while self.get_events() != []:
            pass

    def handle_event(self, event):
        """Gets events resulting from user actions and identifies them."""
        if event.type == MOUSEBUTTONDOWN:
            self.mousebutton_pressed(event)
        elif event.type == MOUSEBUTTONUP:
            self.mousebutton_released(event)
        elif event.type == KEYDOWN:
            self.key_pressed(event)
        elif event.type == KEYUP:
            self.key_released(event)
        elif event.type == QUIT:
            self.exit_signalled(event)
        elif event.type in self.user_events:
            self.user_events[event.type]()

    def event_loop(self):
        """
        Processes events and updates callbacks.
        until no more event listeners are left.
        """
        while self.listeners:
            for event in self.get_events():
                self.handle_event(event)
            for callback in self.callbacks:
                callback.update()
            self.cleanup_listeners()
            pygame.time.delay(self.game_delay)
