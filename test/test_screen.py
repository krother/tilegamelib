
from unittest import TestCase, main
from tilegamelib.screen import Screen
from test_data import RESOLUTION, BACKGROUND_IMAGE, TILE
from util import graphictest, next_frame
import pygame


class ScreenTests(TestCase):
    """
    Tests Screen wrapper.
    """
    def test_attribute(self):
        """Screen has a resolution attribute."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        self.assertEqual(screen.resolution, RESOLUTION)

    @graphictest
    def test_clear(self):
        """Screen can be cleared."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        screen.clear()

    @graphictest
    def test_blit(self):
        """quadratic image is shown, then cleared."""
        screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        bitmap = pygame.image.load(TILE).convert()
        dest = pygame.Rect(60, 60, 32, 32)
        source = pygame.Rect(0, 0, 32, 32)
        screen.blit(bitmap, dest, source)
        next_frame()
        screen.clear()


if __name__ == "__main__":
    main()
