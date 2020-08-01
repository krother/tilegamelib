
import arcade

from tilegamelib import Game
from tilegamelib import TiledMap
from tilegamelib import Vector
from tilegamelib.sprites import TileSprite

MAZE = """##########
#........#
#.#.####.#
#.#......#
#.#....#.#
#.#....#.#
#......#.#
#.####.#.#
#........#
##########"""


class MiniGame(Game):

    def __init__(self):
        super().__init__()

        self.map = TiledMap(self.tiles, MAZE, offset=Vector(96, 96))
        self.map.set((4,4), 'a')
        #self.game.frame.print_text("Hello World", (32, 330))
        self.sprite = TileSprite(self.tiles['b.pac_right'], (1, 2), speed=4, offset=Vector(96, 320))

    def on_draw(self):
        self.map.draw()
        self.sprite.draw()

    def update(self, time_delta):
        self.sprite.update()

    def move(self, direction):
        self.sprite.add_move(direction)


if __name__ == '__main__':
    minigame = MiniGame()
    arcade.run()
