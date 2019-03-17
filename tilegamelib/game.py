
import os
import time
import warnings

from tilegamelib import EventListener, ExitListener, FigureMoveListener
from tilegamelib.config import config
from tilegamelib.draw_timer import draw_timer
from tilegamelib.move_group import MoveGroup


class Game:

    def __init__(self, config_filename=None, quit=True, **kwargs):
        self.config = {}  # deprecated!
        if config_filename:
            self.parse_config(config_filename)
        self.tiles _factory = TileFactory()
        self._exit = False
        self._quit = quit  # terminate PyGame when event loop expires

    def parse_config(self, config_filename):
        """
        Adds contents of config file to config dictionary.
        """
        warnings.warn('Game.parse_config has been deprecated!')
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        before = set(dir())
        conf = open(config_filename).read()
        exec(conf)
        after = set(dir())
        for name in after - before:
            self.config[name] = eval(name)

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
        # if self._quit:
        #    pygame.quit()

    def wait_for_move(self, move=None, draw_func=None, delay=0.01):
        if type(move) is list:
            move = MoveGroup(move)
        while not move.finished:
            move.move()
            if draw_func:
                self.screen.clear()
                draw_func()
            move.draw()
            pygame.display.update()
            time.sleep(delay)
