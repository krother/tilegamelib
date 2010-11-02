#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from pygame.locals import *
from interfaces import Drawable, Updateable, Modal, Commandable
from game_paused import GamePausedBox
from events import EventListener
from screen import GameElement

class GameListener(EventListener):
    
    def is_active(self):
        if self.commandable.is_game_over():
            return False
        return True
    
class Game(Drawable, Updateable, Commandable, Modal, GameElement):
    """Toplevel in-game class managing players."""
    def __init__(self, game_factory):
        GameElement.__init__(self, game_factory)

        self.listener = GameListener(self)
        self.listener.set_command_map({
            self.settings.EXIT_KEY:'quit',
            self.settings.PAUSE_KEY:'pause',
            })
        self.events.add_listener(self.listener)
        self.players = []
        self.highscore = 0
        self.game_over_text = 'Game Over'

    def new_game(self):
        """Starts a game with the set number of players."""
        self.create_players()
        self.set_player_keys()
        self.draw()

    def create_players(self):
        pass

    def terminate(self):
        scores = [p.score for p in self.players]
        if len(scores) == 0:
            self.highscore = 0
        else:
            self.highscore = max(scores)
        self.game_over_text = 'Game Over'
        self.players = []

    def handle_command(self, cmd):
        if cmd == 'quit':
            self.terminate()
            self.events.remove_listener(self.listener)
        elif cmd == 'pause':
            self.pause_game()

    def update(self):
        for p in self.players:
            p.update()
        self.draw()

    def draw(self):
        for p in self.players:
            p.draw()

    def set_player_keys(self):
        """Maps arrow keys to player instances."""
        keys = [self.settings.PLR2_MOVES, \
            self.settings.PLR1_MOVES]
        players = self.players[:]
        players.reverse()
        for player, moves in zip(players, keys):
            elis = EventListener(player)
            elis.set_command_map(moves)
            self.events.add_listener(elis)

    def pause_game(self):
        pause = GamePausedBox(self, 'Game paused - press any key')
        pause.activate()

    def is_game_over(self):
        """Returns whether the game is running"""
        if self.players == []:
            return True
        for p in self.players:
            if p.game_over:
                return True

    def activate(self):
        """Manages the entire game."""
        self.events.add_updateable(self)
        self.events.event_loop()
        self.events.remove_updateable(self)

