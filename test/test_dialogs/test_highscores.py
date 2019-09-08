
import os
from conftest import TEST_DATA_PATH
from tilegamelib.config import config
from tilegamelib.dialogs.highscores import HighscoreBox, HighscoreList
from tilegamelib.events import QUIT_EVENT, EventGenerator
from tilegamelib.frame import Frame


HIGHSCORE_BACKUP = TEST_DATA_PATH + 'test_scores_backup.txt'

config.HIGHSCORE_FILE = TEST_DATA_PATH + 'test_scores.txt'


class HighscoreTests:

    def test_highscore_list(self):
        os.system('cp %s %s' % (HIGHSCORE_BACKUP, config.HIGHSCORE_FILE))
        hl = HighscoreList(config.HIGHSCORE_FILE)
        self.assertFalse(hl.is_in_highscores(10))
        self.assertTrue(hl.is_in_highscores(1000))
        hl.insert_entry('Zergling', 950)
        assert hl.scores[1][0] == 950
        assert hl.scores[1][1] == 'Zergling'

    def test_highscores(self, screen):
        """Enters something into the highscore list."""
        os.system('cp %s %s' % (HIGHSCORE_BACKUP, config.HIGHSCORE_FILE))
        hl = HighscoreList(config.HIGHSCORE_FILE)
        events = EventGenerator()
        events.add_scripted_keys(['B', 'C', chr(K_RETURN), chr(K_RETURN)])
        events.add_scripted_event(QUIT_EVENT)
        screen.clear()
        frame = Frame(screen, config.HIGHSCORE_RECT)
        hs = HighscoreBox(frame, events, hl, config.HIGHSCORE_IMAGE, config.HIGHSCORE_TEXT_POS)
        hs.enter_score(33333)
        hs.activate()
        assert hl.scores[0] == (33333, 'BC')
