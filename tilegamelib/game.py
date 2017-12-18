
import os

from tilegamelib import TileFactory
from tilegamelib.config import config

from .screen import Screen
from .frame import Frame


class Game:

    def __init__(self, config_filename=None, **kwargs):
        self.config = {}  # deprecated!
        if config_filename:
            self.parse_config(config_filename)
        self.screen = Screen()
        self.frame = Frame(self.screen, config.FRAME)
        self.tile_factory = TileFactory()
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
