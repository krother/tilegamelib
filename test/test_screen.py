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
from tilegamelib.screen import Screen, Frame, GameElement
from test_settings import TestSettings, showdoc, TILE, DELAY, TEST_GAME_CONTEXT
import pygame
import time


class ScreenTests(TestCase):
    """
    Tests Screen wrapper.
    """
    def test_clear(self):
        scr = Screen(TestSettings)
        scr.clear()

    @showdoc
    def test_blit(self):
        """quadratic image is shown, then cleared."""
        scr = Screen(TestSettings)
        bitmap = pygame.image.load(TILE).convert()
        dest = pygame.Rect(0, 0, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        scr.blit(bitmap, dest, source)
        pygame.display.update()
        time.sleep(DELAY)
        # clear
        scr.clear()
        pygame.display.update()

class FrameTests(TestCase):

    @showdoc
    def test_frame(self):
        """image and text drawn into frame, then cleared."""
        frame = Frame(TEST_GAME_CONTEXT, (50,50), (100,100))
        # settings property
        self.assertTrue(hasattr(frame.settings,'ORIGIN'))
        # blit method
        bitmap = pygame.image.load(TILE).convert()
        dest = pygame.Rect(32, 16, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        frame.blit(bitmap, dest, source)
        # print text
        frame.print_text('Hello Frame', (50,50), frame.settings.DEMIBOLD_BIG, \
            frame.settings.CYAN )
        pygame.display.update()
        time.sleep(DELAY)
        # clear
        frame.clear()
        pygame.display.update()

    def test_get_dest_rect(self):
        """Adds rectangle values to frame position."""
        frame = Frame(TEST_GAME_CONTEXT, (50,50), (100,100))
        rect = pygame.Rect(10, 20, 20, 31)
        dest = frame.get_dest_rect(rect)
        self.assertEqual(dest, pygame.Rect(60, 70, 20, 31))

    def test_game_element(self):
        """GameElement works as a composite."""
        ge1 = GameElement(TEST_GAME_CONTEXT)
        GameElement(ge1)
     
if __name__ == "__main__":
    main()
