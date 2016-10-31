
from tilegamelib.frame import Frame
from tilegamelib.basic_boxes import ImageBox
from tilegamelib.menu import TextMenuBox
from tilegamelib.events import EventGenerator
import pygame


class TitleScreen:
    """Shows title image and menu."""
    def __init__(self, screen, egen, title_rect, image, menu, menu_rect, moves):
        self.screen = screen
        self.events = egen
        self.events.add_callback(self)
        frame = Frame(self.screen, title_rect)
        self.title = ImageBox(frame, image)
        frame = Frame(self.screen, menu_rect)
        self.menu = TextMenuBox(frame, menu, self.events, moves)

    def update(self):
        self.menu.draw()
        pygame.display.update()

    def run(self):
        """Shows the title menu."""
        self.screen.clear()
        self.title.draw()
        self.menu.draw()
        self.events.event_loop()
        #self.menu.deactivate()
        self.events.remove_callback(self)


def show_title_screen(screen, rect, image, menu, menu_rect, moves):
    # self.settings.KEY_REPEAT = self.settings.MENU_KEY_REPEAT
    events = EventGenerator()
    title = TitleScreen(screen, events, rect, image, menu, menu_rect, moves)
    title.run()
    screen.clear()
    pygame.display.update()