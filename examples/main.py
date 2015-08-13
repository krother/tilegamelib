#! /usr/bin/python

from tilegamelib.game_engine import GameEngine, GameFactory
from tilegamelib.game import Game
from snake import SnakeGame, SnakeFactory
from pac import PacGame, PacFactory
import pygame

class MainSettings(PacSettings):
    MAIN_MENU = [
        ('Pac','create_pac_game'),
        ('Snake','create_snake_game'),
        ('Quit','quit')
        ]

class MainFactory(GameFactory):

    def create_snake_game(self):
        sf = SnakeFactory('snake.conf', factory=self)
        sf.settings.KEY_REPEAT = SnakeSettings.GAME_KEY_REPEAT
        return SnakeGame(sf)

    def create_pac_game(self):
        pf = PacFactory('pac.conf, factory=self)
        pf.settings.KEY_REPEAT = PacSettings.GAME_KEY_REPEAT
        return PacGame(pf)

def main():
    factory = MainFactory()
    engine = GameEngine(factory)
    engine.activate()

if __name__ == '__main__':
    main()
            
