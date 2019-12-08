
import os

import arcade
from arcade import load_texture

from create_stars import STAR_PATH
from tilegamelib.game import Game
from tilegamelib.config import config


class StarScape:
    """Draws a parallax-scrolling background"""
    def __init__(self, path=STAR_PATH):
        self.stars = [
            load_texture(os.path.join(path, 'stars1.png'), 0, 0),
            load_texture(os.path.join(path, 'stars2.png'), 0, 0),
            load_texture(os.path.join(path, 'stars3.png'), 0, 0),
        ]
        self.offsets = [0, 0, 0]
        self.increments = [4, 2, 1]

    def step(self):
        for i in range(3):
            self.offsets[i] += self.increments[i]
            if self.offsets[i] >= 800:
                self.offsets[i] = 0

    def draw(self):
        for i in range(3):
            self.stars[i].draw(self.offsets[i] - 400, 300, 800, 600)
            self.stars[i].draw(self.offsets[i] + 400, 300, 800, 600)


class StarscapeDemo(Game):

    def __init__(self):
        config.TILE_FILE = None
        config.GAME_NAME = 'Starscape'
        config.RESOLUTION = (800, 600)
        super().__init__()
        self.stars = StarScape()

    def update(self, time_delta):
        """called by arcade"""
        self.stars.step()

    def on_draw(self):
        """called by arcade"""
        arcade.start_render()
        self.stars.draw()

if __name__ == '__main__':
    starscape = StarscapeDemo()
    arcade.run()
