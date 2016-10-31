
from .screen import Screen
from tilegamelib import Vector
from tilegamelib.dialogs.title_screen import show_title_screen
from tilegamelib.dialogs.highscores import show_highscores
from tilegamelib.menu import VERTICAL_MOVES
from pygame import Rect
import os


class Game:

    def __init__(self, config_filename, game_class):
        self.game_class = game_class
        self.config = {}
        self.parse_config(config_filename)
        self.screen = Screen(self.config['SCREEN_RESOLUTION'], self.config['SCREEN_BACKGROUND'])
        self._exit = False

    def parse_config(self, config_filename):
        """
        Adds contents of config file to config dictionary.
        """
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        before = set(dir())
        conf = open(config_filename).read()
        exec(conf)
        after = set(dir())
        for name in after - before:
            self.config[name] = eval(name)

    def play(self):
        game = self.game_class(self.screen)
        game.run()
        if self.config['HIGHSCORES']:
            show_highscores(game.score, self.screen,
                rect=self.config['HIGHSCORE_RECT'],
                filename=self.config['HIGHSCORE_FILE'],
                image=self.config['HIGHSCORE_IMAGE'],
                textpos=self.config['HIGHSCORE_TEXTPOS'],
            )

    def exit(self):
        self._exit = True

    def run(self):
        while not self._exit:
            show_title_screen(self.screen, \
                self.config['MAIN_MENU_RECT'],
                self.config['MAIN_MENU_IMAGE'],
                self.config['MAIN_MENU'],
                self.config['MAIN_MENU_TEXTPOS'],
                VERTICAL_MOVES,
            )
