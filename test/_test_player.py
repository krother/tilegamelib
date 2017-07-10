#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


import time
from unittest import main
from unittest import TestCase

import numpy as np
import pygame

from test_settings import showdoc
from test_settings import TEST_GAME_CONTEXT
from test_settings import VERY_SHORT_DELAY
from test_tiled_map import TEST_MAP
from tilegamelib.player import PlayerBox
from tilegamelib.screen import Frame
from tilegamelib.tiled_map import Move

MOVES1 = [
        Move(np.array((0,0)), np.array((0,1)), 3, 2),
        Move(np.array((2,1)), np.array((-1,-1)), 1, 4),
      ]
MOVES2 = [
        Move(np.array((3,3)), np.array((-1,0)), 2, 1),
      ]

class MockPlayer(PlayerBox):

    def __init__(self, frame, context):
        PlayerBox.__init__(self, frame, context)
        self.map.fill_map(TEST_MAP)

class PlayerTests(TestCase):

    @showdoc
    def test_player(self):
        """Two moves across the map shown."""
        frame = Frame(TEST_GAME_CONTEXT, (100,100), (260,260))
        player = MockPlayer(TEST_GAME_CONTEXT, frame)
        player.add_queued_moveset(MOVES1)
        player.add_queued_moveset(MOVES2)
        while player.is_map_moving():
            player.update()
            player.draw()
            pygame.display.update()
            time.sleep(VERY_SHORT_DELAY)
        self.assertEqual(player.score, 0)


if __name__ == "__main__":
    main()
