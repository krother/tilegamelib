#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

from unittest import TestCase, main

from test_interfaces import InterfaceTests
from test_events import EventTests
from test_screen import ScreenTests, FrameTests
from test_sprites import SpriteTests
from test_tiles import TileTests, TileFactoryTests
from test_tiled_map import TiledMapTests, MoveableTiledMapTests
from test_game import GameTests
from test_game_engine import GameEngineTests
from test_basic_boxes import BasicBoxTests
from test_dialogs import GameOverTests, HighscoreTests, GamePausedTests
from test_menu import MenuTests
from test_player import PlayerTests

#from test_game import GameTests
#from test_game_engine import GameEngineTests

if __name__ == '__main__':
    main()
    
