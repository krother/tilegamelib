
from basic_boxes import ImageBox, TextBox
import pygame

class GameOverBox:
    """Displays a game over box."""

    def __init__(self, frame, image, text="Game Over", delay=2500, \
                 offset=None, color=None, font=None, sound=None):
        """Initializes the Game Over Box."""
        self.delay = delay
        self.image = None
        self.sound = sound
        if image:
            self.image = ImageBox(frame, image)
        self.text = TextBox(frame, text, offset, font, color)

    def play_sound(self):
        if self.sound:
            sound.play(snd_name)

    def draw(self):
        if self.image:
            self.image.draw()
        self.text.draw()

    def activate(self):
        self.draw()
        self.play_sound()
        pygame.display.update()
        pygame.time.delay(self.delay)

