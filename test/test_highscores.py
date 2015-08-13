
from unittest import TestCase, main
from tilegamelib.frame import Frame
from tilegamelib.events import EventGenerator, QUIT_EVENT
from tilegamelib.highscores import HighscoreBox, HighscoreList
from test_settings import TestSettings, showdoc, TEST_GAME_CONTEXT, \
     HIGHSCORE_RECT, HIGHSCORE_TEXT_POS, HIGHSCORE_FILE, HIGHSCORE_IMAGE
from pygame import K_RETURN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN,\
        K_ESCAPE
import os


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
        events = EventGenerator(TestSettings)        
        events.add_scripted_keys(['B', 'C', chr(K_RETURN), chr(K_RETURN)])
        events.add_scripted_event(QUIT_EVENT)
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT.screen, HIGHSCORE_RECT)
        hs = HighscoreBox(frame, events, hl, HIGHSCORE_IMAGE, HIGHSCORE_TEXT_POS)
        hs.enter_score(333)
        hs.activate()

if __name__ == '__main__':
    main()
    
