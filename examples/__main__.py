#! /usr/bin/python

from tilegamelib.game import Game
from snake import SnakeGame
from pac import PacGame
from collect_fruit import CollectFruit
from boxes import Boxes
from frutris import frutris


class ExampleGameMenu(Game):

    def create_collect_fruit(self):
        game = Game('data/collect_fruit.conf', CollectFruit)
        game.run()

    def create_box_game(self):
        boxes = Boxes()
        boxes.run()

    def create_snake_game(self):
        game = Game('data/snake.conf', SnakeGame)
        game.run()

    def create_pac_game(self):
        game = Game('data/pac.conf', PacGame)
        game.run()

    def create_frutris(self):
        game = frutris.MainGame('data/frutris.conf', None)
        game.run()


if __name__ == '__main__':
    menu = ExampleGameMenu('data/main.conf', None)
    menu.run()
