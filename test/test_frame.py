
from unittest import main
from unittest import TestCase

from pygame import image
from pygame import Rect

from data import BACKGROUND_IMAGE
from data import DEMIBOLD_BIG
from data import RESOLUTION
from data import TILE
from tilegamelib.frame import Frame
from tilegamelib.screen import Screen
from tilegamelib.vector import Vector
from util import graphictest
from util import next_frame

CYAN = (0, 255, 255)


class FrameTests(TestCase):

    def setUp(self):
        self.screen = Screen(RESOLUTION, BACKGROUND_IMAGE)
        self.frame = Frame(self.screen, Rect(50, 50, 100, 100))

    @graphictest
    def test_blit(self):
        """image drawn into frame, then cleared."""
        bitmap = image.load(TILE).convert()
        dest = Rect(32, 16, 32, 32)
        source = Rect(0, 0, 32, 32)
        self.frame.blit(bitmap, dest, source)
        next_frame()
        self.frame.clear()

    @graphictest
    def test_text(self):
        """Text drawn into frame, then cleared."""
        self.frame.print_text('Hello Frame', Vector(50,50), \
            DEMIBOLD_BIG, CYAN )
        next_frame()
        self.frame.clear()

    def test_get_dest_rect(self):
        """Adds rectangle values to frame position."""
        rect = Rect(10, 20, 20, 31)
        dest = self.frame.get_dest_rect(rect)
        self.assertEqual(dest, Rect(60, 70, 20, 31))

     
if __name__ == "__main__":
    main()
