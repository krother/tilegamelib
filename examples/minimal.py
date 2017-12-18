
import time

import pygame
from pygame import Rect

from tilegamelib import EventGenerator
from tilegamelib import ExitListener
from tilegamelib import FigureMoveListener
from tilegamelib import TiledMap
from tilegamelib import Game
from tilegamelib.draw_timer import draw_timer
from tilegamelib.move_group import MoveGroup
from tilegamelib.map_move import MapMove, wait_for_move
from tilegamelib.sprites import Sprite
from tilegamelib.config import config


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
        pygame.display.update()

    def move(self, direction):
        nearpos = self.player.pos + direction
        near = self.map.at(nearpos)
            
        moves = MoveGroup()
        self.player.add_move(direction)
        moves.add(self.player)

        wait_for_move(moves, self.game.screen, self.draw, 0.005)
        self.draw()

    def run(self):
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    minigame = MiniGame()
    minigame.run()
    pygame.quit()
