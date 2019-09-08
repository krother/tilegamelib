
from tilegamelib.config import config
from tilegamelib.dialogs.game_over import GameOverBox
from tilegamelib.frame import Frame


class GameOverTests:

    def test_game_over(self, screen):
        """Display box with Game Over message."""
        frame = Frame(screen, Rect(100, 100, 260, 160))
        go = GameOverBox(frame, config.GAME_OVER_IMAGE,
            font=config.DEMIBOLD_BIG, color=config.WHITE)
        go.activate()
