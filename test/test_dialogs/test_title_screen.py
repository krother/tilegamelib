
from unittest import TestCase, main
from test_data import TITLE_IMAGE, TITLE_RECT, MENU_RECT
from util import showdoc, TEST_GAME_CONTEXT
from tilegamelib.events import EventGenerator, QUIT_EVENT
from tilegamelib.dialogs.title_screen import TitleScreen
from tilegamelib.menu import VERTICAL_MOVES
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN,\
        K_ESCAPE


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
    
