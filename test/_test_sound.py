#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from unittest import main
from unittest import TestCase

from test_settings import TestSettings
from tilegamelib.sounds import EffectPlayer
from tilegamelib.sounds import MusicPlayer


class SoundTests(TestCase):

    def test_music(self):
        music = MusicPlayer(TestSettings)

    def test_effects(self):
        effects = EffectPlayer(TestSettings)


if __name__ == "__main__":
    main()
