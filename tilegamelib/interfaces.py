#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"

"""
Interface definitions to make good clean design patterns.
"""

class Drawable:
    def draw(self):
        pass

class Updateable:
    def update(self):
        pass

class Modal:
    def activate(self):
        pass

class Commandable:
    def handle_command(self, command):
        pass

    
class GameContext:

    def __init__(self):
        self.screen = None
        self.settings = None
        self.effects = None
        self.music = None
        self.tile_factory = None
        self.events = None
