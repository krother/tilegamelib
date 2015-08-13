

from screen import Screen
from frame import Frame
from tiles import TileFactory
from events import EventGenerator, QUIT_EVENT
from menu import VERTICAL_MOVES

from title_screen import TitleScreen
from game_paused import GamePausedBox
from game_over import GameOverBox
from highscores import HighscoreBox, HighscoreList

from vector import Vector
from sounds import MusicPlayer, EffectPlayer
from settings import read_settings, DEMIBOLD_BIG

import pygame
from pygame.rect import Rect

class GameFactory:
    '''
    Creates game objects based on data from a text file.
    '''
    def __init__(self, filename):
        self.data = read_settings(filename)
        self._screen = None
        self._events = None
        self._tile_factory = None
        self.effects = None
        self.music = None

    @property
    def screen(self):
        if not self._screen:
            resol = self.data['SCREEN_RESOLUTION']
            self._screen = Screen(resol, self.data['SCREEN_BG_IMAGE'])
        return self._screen

    @property
    def event_generator(self):
        if not self._events:
            self._events = EventGenerator(self.data['GAME_DELAY'], self.data['DEFAULT_KEY_REPEAT'])
        return self._events

    @property
    def tile_factory(self):
        if not self._tile_factory:
            self._tile_factory = TileFactory(self.data['TILE_SIZE'], self.data['TILE_SETS'], [])
            #self._tile_factory.add_tile_synonyms(self.data['tile_synonyms'])
        return self._tile_factory

    def get_music_player(self):
        pass
        # return MusicPlayer(self.settings)

    def get_effect_player(self):
        pass
        # return EffectPlayer(self.settings)




