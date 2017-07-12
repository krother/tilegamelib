
import os

from tilegamelib.config import config
from tilegamelib.dialogs.highscores import show_highscores
from tilegamelib.dialogs.title_screen import show_title_screen
from tilegamelib.menu import VERTICAL_MOVES

from .screen import Screen


class Game:

    def __init__(self, config_filename=None):
        self.config = {}  # deprecated!
        if config_filename:
            self.parse_config(config_filename)
        self.screen = Screen()
        self._exit = False

    def parse_config(self, config_filename):
        """
        Adds contents of config file to config dictionary.
        """
        # deprecated!
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        before = set(dir())
        conf = open(config_filename).read()
        exec(conf)
        after = set(dir())
        for name in after - before:
            self.config[name] = eval(name)

    def play(self, game_class):
        game = game_class(self.screen)
        game.run()
        if config.HIGHSCORES:
            show_highscores(game.score, self.screen,
                rect=config.HIGHSCORE_RECT,
                filename=config.HIGHSCORE_FILE,
                image=config.HIGHSCORE_IMAGE,
                textpos=config.HIGHSCORE_TEXT_POS)

    def exit(self):
        self._exit = True

    def main_menu(self):
        while not self._exit:
            show_title_screen(self.screen,
                config.MAIN_MENU_RECT,
                config.MAIN_MENU_IMAGE,
                config.MAIN_MENU,
                config.MAIN_MENU_TEXTPOS,
                VERTICAL_MOVES)
