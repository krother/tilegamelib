
import pytest

from pygame import Rect, image

from test.conftest import TILE
from tilegamelib.config import config
from tilegamelib.frame import Frame
# from util import graphictest, next_frame
from util import next_frame


CYAN = (0, 255, 255)


@pytest.fixture
def frame(screen):
    return Frame(screen, Rect(50, 50, 100, 100))


class TestFrame:
    """Tests for Frame objects"""
    # @graphictest
    def test_blit(self, frame):
        """image drawn into frame, then cleared."""
        bitmap = image.load(TILE).convert()
        dest = Rect(32, 16, 32, 32)
        source = Rect(0, 0, 32, 32)
        frame.blit(bitmap, dest, source)
        next_frame()
        frame.clear()

    # @graphictest
    def test_text(self, frame):
        """Text drawn into frame, then cleared."""
        frame.print_text('Hello Frame', (50, 50),
            config.DEMIBOLD_BIG, config.CYAN)
        next_frame()
        frame.clear()

    def test_get_dest_rect(self, frame):
        """Adds rectangle values to frame position."""
        rect = Rect(10, 20, 20, 31)
        dest = frame.get_dest_rect(rect)
        assert dest == Rect(60, 70, 20, 31)
