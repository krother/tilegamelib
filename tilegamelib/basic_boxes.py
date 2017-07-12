
import time

from pygame import Rect, image

from .config import config
from .frame import Frame
from .vector import Vector


class TextBox(object):
    """Displays a box with text."""
    def __init__(self, frame, text, offset=None, font=None, color=config.WHITE):
        """Initializes the TextBox."""
        self.frame = frame
        self.text = text
        self.font = font
        self.color = color
        self.pos = offset
        if offset is None:
            self.pos = Vector(0, 0)

    def draw(self):
        """Draws the Box."""
        self.frame.clear()
        self.frame.print_text(self.text, self.pos, self.font, self.color)


class ImageBox(object):
    """
    Displays a box with an image.
    """
    def __init__(self, frame, image_fn=None):
        """Initializes the ImageBox."""
        self.frame = frame
        self.image = image.load(image_fn).convert()

    def draw(self):
        """Draws the Box."""
        self.frame.clear()
        self.frame.blit(self.image, self.frame.rect,
                        Rect(0, 0, self.frame.size.x, self.frame.size.y))


class DictBox(object):
    """
    Text window displaying scores etc. taken from a data dictionary
    """
    def __init__(self, frame, data, labels=None):
        self.frame = frame
        self.data = data
        self.labels = labels

    def draw(self):
        """Draws some values from the dictionary."""
        self.frame.clear()
        if self.labels:
            labels = self.labels
        else:
            labels = list(self.data.keys())
            labels.sort()
        for i, lab in enumerate(labels):
            pos = Vector(0, 20 * i)
            self.frame.print_text('{} : {}'.format(lab, str(self.data[lab])), pos)


class FpsBox(TextBox):
    """Displays FPS rate"""
    def __init__(self, screen):
        frame = Frame(screen, Rect(10, 10, 80, 15))
        TextBox.__init__(self, frame, 'fps:', font=config.DEMIBOLD_SMALL, color=config.BLUE)
        self.lasttime = time.time()

    def update(self):
        """
        Measures the time passed since the last call
        and calculates the FPS rate (frames per second).
        """
        now = time.time()
        diff = now - self.lasttime
        self.lasttime = now
        if diff > 0:
            self.text = 'fps: %3.1f' % (1.0 / diff)
