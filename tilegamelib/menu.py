#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from events import EventListener
from interfaces import Drawable, Commandable

class MenuListener(EventListener):
    """Abstract superclass for menu listeners."""
    def is_active(self):
        """Determines when the menu is finished."""
        if self.commandable.result == None:
            return True

class HorizontalMenuListener(MenuListener):

    def __init__(self, commandable, commands):
        MenuListener.__init__(self, commandable)
        self.set_command_map(commands)
        self.rename_command('left','prev')
        self.rename_command('right','next')

class VerticalMenuListener(MenuListener):

    def __init__(self, commandable, commands):
        MenuListener.__init__(self, commandable)
        self.set_command_map(commands)
        self.rename_command('up','prev')
        self.rename_command('down','next')
    

class MenuBox(Drawable, Commandable):
    """
    Abstract superclass for menus on the screen.
    This class manages selecting menu entries and stores
    a selected option in the result field.
    """
    def __init__(self, frame, menu, egen, moves, horizontal=True):
        """
        Creates a game Menu box.
        frame - Frame instance
        menu   - list of (label, result_value) tuples.
        """
        self.frame = frame
        self.menu = menu
        self.highlight = 0
        self.result = None
        self.horizontal = horizontal
        self.egen = egen
        self.listener = self._get_listener(moves)
        self.egen.add_listener(self.listener)

    def destroy(self):
        self.egen.remove_listener(self.listener)

    def _get_listener(self, moves):
        """Returns a MenuListener instance."""
        if self.horizontal:
            return HorizontalMenuListener(self,moves)
        else:
            return VerticalMenuListener(self,moves)
            
    def set_menu(self, menu):
        """applies a new list of menu entries."""
        self.menu = menu

    def handle_command(self, command):
        """Handles selecting things in the menu."""
        if command == 'prev':
            self.choose_previous()
        elif command == 'next':
            self.choose_next()
        elif command == 'select':
            self.select()

    def choose_previous(self):
        self.highlight -= 1
        if self.highlight < 0:
            self.highlight = len(self.menu)-1

    def choose_next(self):
        self.highlight += 1
        if self.highlight == len(self.menu):
            self.highlight = 0

    def select(self):
        self.result = self.menu[self.highlight][1]


class TileMenuBox(MenuBox):

    def __init__(self, factory, frame, menu, egen, moves, horizontal=True, cursor='#'):
        menu = self.create_tiles(menu, factory)
        MenuBox.__init__(self, frame, menu, egen, moves, horizontal)
        self.cursor = factory.get(cursor)

    def create_tiles(self, menu, factory):
        result = []
        for name, value in menu:
            tile = factory.get(name)
            result.append((tile, value))
        return result

    def draw(self):
        """Draws the menu and background image."""
        i = 0
        for tile, value in self.menu:
            x = self.horizontal and i*tile.size[0] or 0
            y = not self.horizontal and i*tile.size[1] or 0
            tile.draw(self.frame, (x,y))
            if self.highlight==i:
                self.draw_cursor((x,y))
            i += 1

    def draw_cursor(self, pos):
        self.cursor.draw(self.frame, pos)


class TextMenuBox(MenuBox):

    def draw(self):
        """Draws the menu and background image."""
        i = 0
        for text, value in self.menu:
            pos = (0,i * 30)
            color = i==self.highlight and self.frame.settings.WHITE or self.frame.settings.BLUE
            self.frame.print_text(text, pos, color=color)
            i += 1
