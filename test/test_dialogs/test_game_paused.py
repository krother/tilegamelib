
from conftest import TEST_DATA_PATH
from tilegamelib.config import config
from tilegamelib.dialogs.game_paused import GamePausedBox
from tilegamelib.events import EventGenerator
from tilegamelib.frame import Frame


config.PAUSE_IMAGE = TEST_DATA_PATH + 'test_tile.png'


class GamePausedTests:

    def test_game_paused(self, screen):
        """Display pause box."""
        frame = Frame(screen, Rect(100, 100, 260, 160))
        egen = EventGenerator()
        egen.add_scripted_keys(['a'])
        gp = GamePausedBox(frame, config.PAUSE_IMAGE, text='test game paused signal', egen=egen)
        gp.draw()
        pygame.display.update()
        gp.activate()
