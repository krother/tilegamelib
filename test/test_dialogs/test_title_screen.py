
from unittest import main
from unittest import TestCase

from pygame import K_DOWN
from pygame import K_ESCAPE
from pygame import K_LEFT
from pygame import K_RETURN
from pygame import K_RIGHT
from pygame import K_SPACE
from pygame import K_UP

from test_data import MENU_RECT
from test_data import TITLE_IMAGE
from test_data import TITLE_RECT
from tilegamelib.dialogs.title_screen import TitleScreen
from tilegamelib.events import EventGenerator
from tilegamelib.events import QUIT_EVENT
from tilegamelib.menu import VERTICAL_MOVES
from util import showdoc
from util import TEST_GAME_CONTEXT


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
                
    @showdoc
    def test_show_title(self):
        """Displays a main menu."""
        menu = [
            ('One', self.one),
            ('Two', self.two),
            ('Three', self.three),
            ]
        title = TitleScreen(TEST_GAME_CONTEXT.screen, self.events, \
                            TITLE_RECT, TITLE_IMAGE, menu, MENU_RECT, VERTICAL_MOVES)
        self.events.add_scripted_keys([K_UP, K_RETURN, K_DOWN, K_DOWN, \
                                       K_SPACE, K_RETURN, K_UP, K_RETURN, K_UP])
        self.events.add_scripted_event(QUIT_EVENT)
        title.run()
        self.assertEqual(self.result, '3221')

if __name__ == '__main__':
    main()
