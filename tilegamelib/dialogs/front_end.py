
from tilegamelib.config import config
from tilegamelib.dialogs.highscores import show_highscores
from tilegamelib.dialogs.title_screen import show_title_screen
from tilegamelib.menu import VERTICAL_MOVES


class FrontEnd:

    def __init__(self):
        self._exit = False

    def play(self, game_class):
        game = game_class(self.screen, self.tile_factory)
        game.run()
        if config.HIGHSCORES:
            show_highscores(game.score, self.screen,
                rect=config.HIGHSCORE_RECT,
                filename=config.HIGHSCORE_FILE,
                image=config.HIGHSCORE_IMAGE,
                textpos=config.HIGHSCORE_TEXT_POS)

    def exit(self):
        self._exit = True

    def main_menu(self):
        while not self._exit:
            show_title_screen(self.screen,
                config.MAIN_MENU_RECT,
                config.MAIN_MENU_IMAGE,
                config.MAIN_MENU,
                config.MAIN_MENU_TEXTPOS,
                VERTICAL_MOVES)
