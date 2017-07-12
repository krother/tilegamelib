
import os
from unittest import TestCase, main

from pygame import K_RETURN

from conftest import TEST_DATA_PATH
from test.util import TEST_GAME_CONTEXT, showdoc
from tilegamelib.config import config
from tilegamelib.dialogs.highscores import HighscoreBox, HighscoreList
from tilegamelib.events import QUIT_EVENT, EventGenerator
from tilegamelib.frame import Frame


HIGHSCORE_BACKUP = TEST_DATA_PATH + 'test_scores_backup.txt'

config.HIGHSCORE_FILE = TEST_DATA_PATH + 'test_scores.txt'


class HighscoreTests(TestCase):

    def test_highscore_list(self):
        os.system('cp %s %s' % (HIGHSCORE_BACKUP, config.HIGHSCORE_FILE))
        hl = HighscoreList(config.HIGHSCORE_FILE)
        self.assertFalse(hl.is_in_highscores(10))
        self.assertTrue(hl.is_in_highscores(1000))
        hl.insert_entry('Zergling', 950)
        self.assertEqual(hl.scores[1][0], 950)
        self.assertEqual(hl.scores[1][1], 'Zergling')

    @showdoc
    def test_highscores(self):
        """Enters something into the highscore list."""
        os.system('cp %s %s' % (HIGHSCORE_BACKUP, config.HIGHSCORE_FILE))
        hl = HighscoreList(config.HIGHSCORE_FILE)
        events = EventGenerator()
        events.add_scripted_keys(['B', 'C', chr(K_RETURN), chr(K_RETURN)])
        events.add_scripted_event(QUIT_EVENT)
        TEST_GAME_CONTEXT.screen.clear()
        frame = Frame(TEST_GAME_CONTEXT.screen, config.HIGHSCORE_RECT)
        hs = HighscoreBox(frame, events, hl, config.HIGHSCORE_IMAGE, config.HIGHSCORE_TEXT_POS)
        hs.enter_score(33333)
        hs.activate()
        self.assertEqual(hl.scores[0], (33333, 'BC'))

if __name__ == '__main__':
    main()
