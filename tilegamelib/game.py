
import os
import time

from tilegamelib.config import config
from tilegamelib import PLAYER_MOVES
from tilegamelib.tiled_map import load_tiles
import arcade
from arcade.key import ESCAPE


class Game(arcade.Window):
    """
    Simple game class for tile-based games
    """
    def __init__(self):
        super().__init__(config.RESOLUTION[0], config.RESOLUTION[1], config.GAME_NAME)
        self.tiles = load_tiles(config.TILE_FILE)

    def exit(self):
        time.sleep(2)
        arcade.window_commands.close_window()

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        vec = PLAYER_MOVES.get(symbol)
        if vec:
            self.move(vec)
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()
