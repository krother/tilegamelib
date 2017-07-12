
import pygame

from tilegamelib.basic_boxes import ImageBox, TextBox


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


def show_game_over():
    """Displays the game over box for some time."""
    self.final_score = final_score
    frame = Frame(self.screen, self.data['GAME_OVER_RECT'])
    game_over = GameOverBox(frame, self.data['GAME_OVER_IMAGE'], text, \
                self.data['GAME_OVER_DELAY'], self.data['GAME_OVER_OFFSET'], \
                self.data['GAME_OVER_COLOR'], DEMIBOLD_BIG)
    game_over.activate()
