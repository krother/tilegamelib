#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from tiled_map import MoveableTiledMap, SpriteList
from interfaces import Drawable, Updateable, Commandable
from screen import GameElement
    
class PlayerBox(Drawable, Updateable, Commandable, GameElement):
    """
    Part of the screen where the game takes place, controlled by one
    player. That part of the screen is to be filled by tiles.
    Each PlayerBox controls a TiledStaticMap that contains background tiles,
    and a TiledSpriteMap that contains moving elements.
    """
    def __init__(self, game_factory, frame):
        """
        Creates a PlayerBox instance.
        Parameters:
        """
        GameElement.__init__(self, game_factory)
        self.frame = frame
        self.map = MoveableTiledMap(game_factory, frame)
        self.sprites = SpriteList()
        self.move_queue = []
        self.score = 0

    @property
    def game_over(self):
        return False

    def update(self):
        """Updates the 2D map and sprites."""
        self.map.update()
        self.sprites.update()
        if not self.map.are_tiles_moving() and self.move_queue:
            moveset = self.move_queue.pop(0)
            for move in moveset:
                self.map.move_tile(move)

    def add_queued_moveset(self,moves):
        self.move_queue.append(moves)

    def is_map_moving(self):
        return self.move_queue or self.map.are_tiles_moving()

    def draw(self):
        """Draws the 2D map and sprites."""
        self.map.draw()
        self.sprites.draw()


