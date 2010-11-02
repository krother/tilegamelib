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
from tilegamelib.interfaces import Drawable, Updateable, Modal, Commandable,\
    GameContext

class InterfaceTests(TestCase):
    """
    Tests existence of basic interfaces.
    """
    def test_drawable(self):
        """Drawable interface exists."""
        obj = Drawable()
        obj.draw()

    def test_updateable(self):
        """Updateable interface exists."""
        obj = Updateable()
        obj.update()

    def test_modal(self):
        obj = Modal()
        obj.activate()

    def test_commandable(self):
        obj = Commandable()
        obj.handle_command("do_something")

    def test_game_context(self):
        obj = GameContext()
        self.assertEqual(obj.screen, None)
        self.assertEqual(obj.settings, None)
        self.assertEqual(obj.tile_factory, None)
        self.assertEqual(obj.effects, None)
        self.assertEqual(obj.music, None)
        self.assertEqual(obj.events, None)


if __name__ == "__main__":
    main()
