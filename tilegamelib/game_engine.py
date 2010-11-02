#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


import pygame
from interfaces import Updateable, Modal
from screen import Screen, Frame, GameElement
from tiles import TileFactory
from events import EventGenerator
from menu import TextMenuBox
from game_over import GameOverBox
from highscores import HighscoreBox
from basic_boxes import ImageBox
from game import Game
from sounds import MusicPlayer, EffectPlayer
from interfaces import GameContext

class GameFactory(GameContext):
    """
    Produces all objects needed by GameEngine.
    """
    def __init__(self, settings):
        GameContext.__init__(self)
        self.settings = settings
        self.screen = self.create_screen()
        self.tile_factory = self.create_tile_factory()
        self.events = self.create_effect_player()
        self.music = self.create_music_player()
        self.events = self.create_event_generator()

    def create_screen(self):
        return Screen(self.settings)

    def create_tile_factory(self):
        return TileFactory(self.settings)

    def create_event_generator(self):
        return EventGenerator(self.settings)

    def create_main_menu(self):
        frame = Frame(self, self.settings.MAIN_MENU_POS, self.settings.MAIN_MENU_SIZE)
        return TextMenuBox(frame, self.settings.MAIN_MENU, self.events, \
            self.settings.MENU_MOVES,horizontal=False)

    def create_one_player_game(self):
        return Game(self)

    def create_two_player_game(self):
        return Game(self)

    def create_game(self, gametype):
        if gametype == 'one player game':
            return self.create_one_player_game()
        elif gametype == 'two player game':
            return self.create_two_player_game()
        else:
            raise Exception("Nonexistent game type: %s"%gametype)

    def create_game_over(self, text):
        frame = Frame(self, self.settings.GAME_OVER_POS, self.settings.GAME_OVER_SIZE)
        return GameOverBox(self, frame, text)

    def create_highscores(self):
        frame = Frame(self, self.settings.HIGHSCORE_POS, self.settings.HIGHSCORE_SIZE)
        return HighscoreBox(self, frame, self.events)

    def create_music_player(self):
        return MusicPlayer(self.settings)

    def create_effect_player(self):
        return EffectPlayer(self.settings)


class GameEngine(Updateable, Modal, GameElement):
    """Main Class managing events and the game architecture."""
    def __init__(self, game_factory):
        GameElement.__init__(self, game_factory)
        self.events.add_updateable(self)
        self.menu = None
        self.game = None

    def show_menu(self):
        self.screen.clear()
        frame = Frame(self.context, self.settings.TITLE_POS, self.settings.TITLE_SIZE)
        title = ImageBox(frame, self.settings.TITLE_IMAGE)
        title.draw()
        self.menu = self.context.create_main_menu()
        self.events.event_loop()
        result = self.menu.result
        self.menu = None
        return result

    def update(self):
        if self.menu!=None:
            self.menu.draw()
        if self.game:
            self.game.update()
        pygame.display.update()

    def show_game(self, result):
        self.screen.clear()
        # game
        game = self.context.create_game(result)
        game.new_game()
        game.activate()
        game.terminate()
        # Game Over
        self.show_game_over(game.game_over_text)
        # High scores
        self.show_highscores(game.highscore)

    def show_game_over(self,text):
        """Displays the game over box for some time."""
        self.screen.clear()
        game_over = self.context.create_game_over(text)
        game_over.activate()

    def show_highscores(self, new_score=0):
        """
        Displays the high score list and
        lets enter a name if the score is high enough.
        """
        self.screen.clear()
        hs = self.context.create_highscores()
        hs.enter_score(new_score)
        hs.activate()

    def activate(self):
        result = self.show_menu()
        while not result=='quit':
            self.show_game(result)
            result = self.show_menu()
