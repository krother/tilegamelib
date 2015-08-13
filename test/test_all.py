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

from test_vector import VectorTests
from test_events import EventTests, AnyKeyListenerTests, TextEnteringListenerTests
from test_screen import ScreenTests
from test_frame import FrameTests
from test_sprites import SpriteTests, SpriteListTests
from test_animation import AnimationTests
from test_tiles import TileTests, TileFactoryTests

from test_tiled_map import TiledMapTests, MoveableTiledMapTests
from test_basic_boxes import BasicBoxTests
from test_game_over import GameOverTests
from test_game_paused import GamePausedTests
from test_title_screen import TitleScreenTests
from test_highscores import HighscoreTests
from test_menu import TextMenuTests, TileMenuTests


if __name__ == '__main__':
    main()
    
