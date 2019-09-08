"""
Helper functions for testing
"""

import time

#from tilegamelib import Frame, Game, Screen, TileFactory
#from tilegamelib.basic_boxes import TextBox
from tilegamelib.config import config



def showdoc(func):
    """
    decorator function showing a docstring
    """
    def do_show(self, *args):
        """Clear screen, show docstring, run test."""
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT.screen, Rect(10, 400, 400, 50))
        tb = TextBox(frame, func.__doc__)
        tb.draw()
        pygame.display.update()
        func(self, *args)
        next_frame()
    return do_show


def graphictest(func):
    """
    decorator function updating display and waiting
    """
    def wrap_test(self):
        func(self)
        next_frame()

    return wrap_test
