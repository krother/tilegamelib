
import os

import arcade
from arcade import load_texture

from tilegamelib.starscape import STAR_PATH
from tilegamelib.game import Game
from tilegamelib.config import config


class StarScape:
    """Draws a parallax-scrolling background"""
    def __init__(self, path=STAR_PATH, size=(800, 600), delay=1):
        suffix = '' if size[0] == 800 else 'b'
        print(suffix)
        self.stars = [
            load_texture(os.path.join(path, f'stars1{suffix}.png'), 0, 0),
            load_texture(os.path.join(path, f'stars2{suffix}.png'), 0, 0),
            load_texture(os.path.join(path, f'stars3{suffix}.png'), 0, 0),
        ]
        self.offsets = [0, 0, 0]
        self.increments = [4, 2, 1]
        self.xsize, self.ysize = size
        self.delay = delay
        self.counter = delay

    def step(self):
        self.counter -= 1
        if self.counter != 0:
            return
        self.counter = self.delay
        for i in range(3):
            self.offsets[i] += self.increments[i]
            if self.offsets[i] >= self.xsize:
                self.offsets[i] = 0

    def draw(self):
        for i in range(3):
            self.stars[i].draw(self.offsets[i] - self.xsize // 2, self.ysize // 2, self.xsize, self.ysize)
            self.stars[i].draw(self.offsets[i] + self.xsize // 2, self.ysize // 2, self.xsize, self.ysize)


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
