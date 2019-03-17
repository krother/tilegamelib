
import os
import time

#from tilegamelib import EventListener, ExitListener, FigureMoveListener
from tilegamelib.config import config
from tilegamelib.move_group import MoveGroup
from


class Game:
    """
    Simple game class
    """
    def __init__(self, quit=True):
        self.tiles = load_tiles(config.tile_file)
        self.exit = False

    def event_loop(self, figure_moves=None, exit=True, draw_func=None, keymap=None, delay=20):
        self.events = EventGenerator()
        if figure_moves:
            self.events.add_listener(FigureMoveListener(figure_moves))
        if keymap:
            self.events.add_listener(EventListener(keymap=keymap))
        if exit:
            self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(draw_func, self.events, delay=delay):
            self.events.event_loop()

    def exit(self):
        self.events.exit_signalled()
