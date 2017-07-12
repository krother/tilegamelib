
import os
import time

import pygame
import pygame.mixer


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

CHANNELS = {}
MUSIC = {}
STARTED_TIME = [0]

STILL_PLAYING = True
CLOSE_TO_END = False
WARN_BEFORE = 5.0


class MusicPlayer:

    def check_music_status(self):
        """
        Checks the queue status.
        Reinitializes the timer.
        Returns a warning if there are only some seconds to go.
        *** depends on being checked regularly. ***
        """
        if not MUSIC[0].get_queue():
            # reinitialize timer
            if STARTED_TIME[0] == 0:
                STARTED_TIME[0] = time.time()
            # check timer and generate warning
            sound = MUSIC[0].get_sound()
            if sound is not None:
                length = sound.get_length()
            else:
                length = 0
            passed = time.time() - STARTED_TIME[0]
            if length - passed <= WARN_BEFORE:
                return CLOSE_TO_END
        return STILL_PLAYING

    def play_music(self, filename, volume=1.0):
        """Starts a new music"""
        if not os.path.exists(filename):
            raise IOError("File '%s' not found!" % filename)
        filename = '/home/krother/projects/frutris/frutris/music/a1.ogg'
        sound = pygame.mixer.Sound(filename)
        c = pygame.mixer.Channel(1)
        c.set_volume(volume)
        c.play(sound)
        MUSIC[0] = c
        print('playing', filename)
        STARTED_TIME[0] = 0

    def next_music(self, filename):
        if MUSIC[0].get_queue():
            print("QUEUE FULL")
            return
        sound = pygame.mixer.Sound(filename)
        MUSIC[0].queue(sound)
        STARTED_TIME[0] = 0

    def stop_music(self):
        if 0 in MUSIC:
            MUSIC[0].fadeout(2)
        # MUSIC[0] = None


def play_effect(filename):
    if not os.access(filename, os.F_OK):
        print('file not found', filename)
        return
    channel = pygame.mixer.find_channel(2)
    channel.stop()
    channel.set_volume(1.0)
    # channel.set_volume(1.0, 1.0)
    sound = pygame.mixer.Sound(filename)
    channel.play(sound)
    CHANNELS[0] = channel
