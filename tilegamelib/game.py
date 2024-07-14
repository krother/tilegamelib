
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
        arcade.set_background_color(config.BG_COLOR)
        if config.TILE_FILE:
            self.tiles = load_tiles(config.TILE_FILE)
        self.keymap = PLAYER_MOVES

    def exit(self):
        self.on_draw()
        time.sleep(2)
        arcade.window_commands.close_window()

    def on_key_press(self, symbol, mod):
        """Handle player movementmap"""
        vec = self.keymap.get(symbol)
        if vec:
            self.move(vec)
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()
