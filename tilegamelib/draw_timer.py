
from contextlib import contextmanager

import pygame
from pygame.locals import USEREVENT


@contextmanager
def draw_timer(callback, event_generator, delay=20, draw_event=USEREVENT):
    dt = DrawTimer(callback, event_generator, delay, draw_event)
    dt.start_timer()
    yield
    dt.stop_timer()


class DrawTimer:

    def __init__(self, callback, event_generator, delay=20, draw_event=USEREVENT):
        self.egen = event_generator
        self.callbacks = [callback]
        self.draw_event = draw_event
        self.delay = delay

    def draw(self):
        for c in self.callbacks:
            c.draw()
        pygame.display.update()

    def start_timer(self):
        self.egen.user_events[self.draw_event] = self.draw
        pygame.time.set_timer(self.draw_event, self.delay)

    def stop_timer(self):
        pygame.time.set_timer(self.draw_event, 0)
        del self.egen.user_events[self.draw_event]
