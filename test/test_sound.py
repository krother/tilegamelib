
from unittest import TestCase, main

from tilegamelib.config import config
# from tilegamelib.sounds import play_effect
from tilegamelib.sounds import MusicPlayer


class SoundTests(TestCase):

    def test_music(self):
        music = MusicPlayer()
        music.play_music(config.BASE_PATH + '/../examples/music/a1.mp3')
        music.stop_music()

    # def test_effects(self):
    #    play_effect('bla')


if __name__ == "__main__":
    main()
