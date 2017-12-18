
from pygame import K_DELETE
from pygame import K_DOWN
from pygame import K_ESCAPE
from pygame import K_LEFT
from pygame import K_RETURN
from pygame import K_RIGHT
from pygame import K_UP

from .vector import DOWN
from .vector import LEFT
from .vector import RIGHT
from .vector import UP


class EventListener:
    """
    Manages callback functions for handling events.
    """
    def __init__(self, keymap=None, leftclick=None, rightclick=None):
        self.keymap = keymap or {}
        self.onleft = leftclick
        self.onright = rightclick
        self.terminated = False

    def leftclick(self, pos):
        """Called each time the left mouse button is clicked."""
        if self.onleft:
            return self.onleft(pos)

    def rightclick(self, pos):
        """Called each time the right mouse button is clicked."""
        if self.onright:
            return self.onright(pos)

    def handle_key(self, key):
        """Called each time a key event needs to be handled."""
        func = self.keymap.get(key)
        if func:
            func()
            return True
        return None

    def terminate(self):
        """Instructs the event loop to deactivate the listener"""
        self.terminated = True


class AnyKeyListener(EventListener):
    """
    Responds to any key.
    """
    def __init__(self, callback):
        EventListener.__init__(self)
        self.callback = callback

    def handle_key(self, key):
        self.callback()
        self.terminate()
        return True


class TextEnteringListener(EventListener):
    """
    Collects text from keyboard until enter is pressed.
    """
    def __init__(self, entered, finished, upper=True):
        EventListener.__init__(self)
        self.text = ''
        self.entered = entered
        self.finished = finished
        self.upper = upper

    def handle_key(self, key):
        """Name entering."""
        if key == K_RETURN:
            self.finished(self.text)
            self.terminate()
        elif key == K_DELETE:
            self.text = self.text[:-1]
            self.entered(self.text)
        elif 64 < key < 200:
            self.text += chr(key)
            if self.upper:
                self.text = self.text.upper()
            self.entered(self.text)


ARROWS = [K_LEFT, K_RIGHT, K_UP, K_DOWN]


class FigureMoveListener(EventListener):
    """Moves a figure according to pressed keys"""
    def __init__(self, callback, keys=ARROWS):
        EventListener.__init__(self, keymap={
            keys[0]: self.left,
            keys[1]: self.right,
            keys[2]: self.up,
            keys[3]: self.down})
        self.callback = callback

    def up(self):
        self.callback(UP)

    def down(self):
        self.callback(DOWN)

    def left(self):
        self.callback(LEFT)

    def right(self):
        self.callback(RIGHT)


class ExitListener(EventListener):
    def __init__(self, callback):
        EventListener.__init__(self, keymap={K_ESCAPE: callback})
