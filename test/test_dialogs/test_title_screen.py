
from unittest import TestCase, main

from pygame import K_DOWN, K_RETURN, K_SPACE, K_UP

from conftest import MENU_RECT, TITLE_IMAGE, TITLE_RECT
from tilegamelib.dialogs.title_screen import TitleScreen
from tilegamelib.events import QUIT_EVENT, EventGenerator
from tilegamelib.menu import VERTICAL_MOVES


class TitleScreenTests(TestCase):

    def setUp(self):
        self.events = EventGenerator()
        self.result = ''

    def one(self):
        self.result += '1'

    def two(self):
        self.result += '2'

    def three(self):
        self.result += '3'

    def test_show_title(self, screen):
        """Displays a main menu."""
        menu = [
            ('One', self.one),
            ('Two', self.two),
            ('Three', self.three),
        ]
        title = TitleScreen(screen, self.events,
                            TITLE_RECT, TITLE_IMAGE, menu, MENU_RECT, VERTICAL_MOVES)
        self.events.add_scripted_keys([K_UP, K_RETURN, K_DOWN, K_DOWN,
                                       K_SPACE, K_RETURN, K_UP, K_RETURN, K_UP], converter=int)
        self.events.add_scripted_event(QUIT_EVENT)
        title.run()
        self.assertEqual(self.result, '3')

if __name__ == '__main__':
    main()
