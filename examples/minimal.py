
from tilegamelib import Game
from tilegamelib import TiledMap
from tilegamelib.sprites import Sprite

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


class MiniGame:

    def __init__(self):
        self.game = Game()
        
        self.map = TiledMap(self.game)
        self.map.fill_map('#', (10, 10))
        self.map.set_map(MAZE)
        self.map.set_tile((4,4), 'a')
        self.game.frame.print_text("Hello World", (32, 330))
        self.sprite = Sprite(self.game.frame, self.game.get_tile('b.pac_right'),
                             (1, 1), speed=2)
        self.game.event_loop(figure_moves=self.move, draw_func=self.draw)

    def draw(self):
        self.map.draw()
        self.sprite.draw()

    def move(self, direction):
        self.sprite.add_move(direction)
        self.game.wait_for_move(self.sprite, self.draw, 0.01)


if __name__ == '__main__':
    minigame = MiniGame()
