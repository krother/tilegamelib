
from unittest import main
from unittest import TestCase

from pygame import K_RETURN
from pygame import K_SPACE

from tilegamelib.events import QUIT_EVENT
from tilegamelib.game_factory import GameFactory


class GameFactoryTests(TestCase):

    def test_game_factory(self):
        """factory creates in-game objects."""
        gf = GameFactory('test_data/settings.txt')
        screen = gf.screen
        ev = gf.event_generator
        tf = gf.tile_factory
        mu = gf.get_music_player()
        ef = gf.get_effect_player()

    def test_dialogs(self):
        """factory creates in-game dialogs."""
        gf = GameFactory('test_data/settings.txt')
        gf.event_generator.add_scripted_event(QUIT_EVENT)
        gf.show_title_screen()
        gf.event_generator.add_scripted_keys('a')
        gf.show_pause_game()
        gf.show_game_over('test game over')
        gf.event_generator.add_scripted_keys('Abathur')
        gf.event_generator.add_scripted_keys(chr(K_RETURN))
        gf.event_generator.add_scripted_keys(chr(K_SPACE))
        gf.show_highscores(950)


if __name__ == "__main__":
    main()
