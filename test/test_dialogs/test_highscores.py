
import os
from unittest import main
from unittest import TestCase

from pygame import K_DOWN
from pygame import K_ESCAPE
from pygame import K_LEFT
from pygame import K_RETURN
from pygame import K_RIGHT
from pygame import K_SPACE
from pygame import K_UP

from test_data import HIGHSCORE_FILE
from test_data import HIGHSCORE_IMAGE
from test_data import HIGHSCORE_RECT
from test_data import HIGHSCORE_TEXT_POS
from tilegamelib.dialogs.highscores import HighscoreBox
from tilegamelib.dialogs.highscores import HighscoreList
from tilegamelib.events import EventGenerator
from tilegamelib.events import QUIT_EVENT
from tilegamelib.frame import Frame
from util import showdoc
from util import TEST_GAME_CONTEXT

HIGHSCORE_BACKUP = 'test_data/test_scores_backup.txt'

class HighscoreTests(TestCase):

    def setUp(self):
        os.system('cp %s %s'%(HIGHSCORE_BACKUP, HIGHSCORE_FILE))

    def test_highscore_list(self):
        hl = HighscoreList(HIGHSCORE_FILE)
        self.assertFalse(hl.is_in_highscores(10))
        self.assertTrue(hl.is_in_highscores(1000))
        hl.insert_entry('Zergling', 950)
        self.assertEqual(hl.scores[1][0], 950)
        self.assertEqual(hl.scores[1][1], 'Zergling')
        
    @showdoc
    def test_highscores(self):
        """Enters something into the highscore list."""
        hl = HighscoreList(HIGHSCORE_FILE)
        events = EventGenerator()        
        events.add_scripted_keys(['B', 'C', chr(K_RETURN), chr(K_RETURN)])
        events.add_scripted_event(QUIT_EVENT)
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT.screen, HIGHSCORE_RECT)
        hs = HighscoreBox(frame, events, hl, HIGHSCORE_IMAGE, HIGHSCORE_TEXT_POS)
        hs.enter_score(333)
        self.assertEqual(hl.scores[0],(333,'BC'))
        hs.activate()

if __name__ == '__main__':
    main()
