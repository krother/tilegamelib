
from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RETURN, K_RIGHT, K_SPACE, K_UP

from .config import config
from .event_listener import EventListener
from .vector import Vector


VERTICAL_MOVES = [K_ESCAPE, K_UP, K_DOWN, K_RETURN, K_SPACE]
HORIZONTAL_MOVES = [K_ESCAPE, K_LEFT, K_RIGHT, K_RETURN, K_SPACE]


class MenuBox:
    """
    Abstract superclass for menus on the screen.
    This class manages selecting menu entries and stores
    a selected option in the result field.
    """
    def __init__(self, frame, menu, egen, moves):
        """
        Creates a game Menu box.
        frame - Frame instance
        menu   - list of (label, callback) tuples.
        egen - EventGenerator object
        """
        self.frame = frame
        self.menu = menu
        self.active = 0
        self.result = None
        self.egen = egen
        self.listener = self.get_listener(moves)
        self.egen.add_listener(self.listener)

    def get_listener(self, moves):
        callbacks = [self.deactivate, self.prev_item, self.next_item,
            self.select, self.select]
        keymap = dict(zip(moves, callbacks))
        return EventListener(keymap=keymap)

    def select(self):
        """Handles selecting things in the menu."""
        callback = self.menu[self.active][1]
        callback()
        self.deactivate()

    def prev_item(self):
        self.active -= 1
        if self.active < 0:
            self.active = len(self.menu) - 1

    def next_item(self):
        self.active += 1
        if self.active == len(self.menu):
            self.active = 0

    def deactivate(self):
        self.egen.remove_listener(self.listener)


class TileMenuBox(MenuBox):

    def __init__(self, factory, frame, menu, egen, moves, horizontal=True, cursor='#'):
        menu = self.create_tiles(menu, factory)
        MenuBox.__init__(self, frame, menu, egen, moves)
        self.horizontal = horizontal
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
            x = self.horizontal and i * tile.size.x or 0
            y = not self.horizontal and i * tile.size.y or 0
            tile.draw(self.frame, Vector(x, y))
            if self.active == i:
                self.draw_cursor(Vector(x, y))
            i += 1

    def draw_cursor(self, pos):
        self.cursor.draw(self.frame, pos)


class TextMenuBox(MenuBox):

    def __init__(self, frame, menu, egen, moves, color=config.BLUE,
            highlight=config.WHITE):
        MenuBox.__init__(self, frame, menu, egen, moves)
        self.color = color
        self.highlight = highlight

    def draw(self):
        """Draws the menu and background image."""
        i = 0
        for text, value in self.menu:
            pos = Vector(0, i * 30)
            if i == self.active:
                col = self.highlight
            else:
                col = self.color
            self.frame.print_text(text, pos, color=col)
            i += 1
