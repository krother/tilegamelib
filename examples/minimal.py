
import pygame
from pygame import Rect

from tilegamelib import TiledMap
from tilegamelib import Game
from tilegamelib.move_group import MoveGroup
from tilegamelib.sprites import Sprite


class MiniGame:

    def __init__(self):
        self.game = Game()
        self.map = TiledMap(self.game.frame, self.game.tile_factory)
        self.map.fill_map('#', (10, 10))
        self.player = Sprite(self.game.frame, self.game.tile_factory.get('b.tail'),
                             (4, 1), speed=2)

    def draw(self):
        self.map.draw()
        self.player.draw()

    def move(self, direction):
        nearpos = self.player.pos + direction
        near = self.map.at(nearpos)
            
        self.player.add_move(direction)
        self.game.wait_for_move(self.player, self.draw, 0.005)

    def run(self):
        self.game.event_loop(figure_moves=self.move, draw_func=self.draw)


if __name__ == '__main__':
    minigame = MiniGame()
    minigame.run()
    pygame.quit()
