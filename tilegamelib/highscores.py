#!/usr/bin/env python
#
# Copyright 2010 Kristian Rother
#
# All rights reserved.
# Please see the LICENSE file that should have been included
# as part of this package.

__author__="Kristian Rother"
__email__ ="krother@rubor.de"


from interfaces import Drawable, Commandable, Updateable,Modal
from basic_boxes import ImageBox
from game_paused import AnyKeyListener
from events import EventListener
from screen import GameElement
import pygame

"""
Uses the MCV pattern

TextEnteringListener - Controller
HighscoreList - Model
HighscoreBox - View
"""

class TextEnteringListener(EventListener):
    """
    Controller for High Scores.
    Collects text entered until enter is pressed.
    """
    def __init__(self,commandable,settings):
        EventListener.__init__(self,commandable)
        self.settings = settings
        self.entering = True
        self.text = ''

    def is_active(self):
        return self.entering

    def handle_key(self, key):
        """Name entering."""
        if self.entering:
            if key == self.settings.ENTER_KEY:
                self.entering = False
                self.commandable.handle_command('text:'+self.text)
            elif key == self.settings.BACKSPACE_KEY:
                self.text = self.text[:-1]
            elif 64 < key <200:
                # force upppercase
                self.text += chr(key).upper()
                self.commandable.handle_command('text:'+self.text)


class HighscoreList:
    """Model for the highscores."""
    def __init__(self, settings):
        self.filename = settings.HIGHSCORE_FILE
        self.length = settings.HIGHSCORE_LENGTH
        self.scores = []
        self.load_scores()

    def load_scores(self):
        self.scores = []
        for line in open(self.filename):
            score,name = line.strip().split()
            self.scores.append((int(score),name))

    def write_scores(self):
        out = []
        for score,name in self.scores:
            print score,name
            out.append('%i\t%s\n'%(score,name))
        open(self.filename,'w').writelines(out)

    def is_in_highscores(self,score):
        """Returns true if the given score gets into the list."""
        if score > self.scores[-1][0]:
            return True

    def insert_entry(self, name, score):
        if name.strip()=='':
            name='ANONYMOUS'
        self.scores.append((score,name))
        self.scores.sort()
        self.scores.reverse()
        self.scores = self.scores[:self.length]
        self.write_scores()

class HighscoreBox(Drawable, Commandable, Updateable, Modal, GameElement):
    """
    View for high scores.
    This class manages entering names
    and storing the high scores in a file.
    """
    def __init__(self, context, frame, egen):
        """
        frame - Frame instance
        egen - EventGenerator instance
        """
        GameElement.__init__(self, context)
        self.frame = frame
        self.egen = egen
        self.highscores = HighscoreList(self.settings)
        self.image = ImageBox(frame, self.settings.HIGHSCORE_IMAGE)
        
        # for entering new entries
        self.entered_name = ""
        self.entered_score = 0

    def handle_command(self, cmd):
        if cmd.startswith('text:'):
            self.entered_name = cmd[5:]

    def draw(self):
        """Draws the highscore list."""
        self.image.draw()
        i = 0
        for score,name in self.highscores.scores:
            y_offset = i * 30
            text = "%8i - %s"%(score,name)
            self.frame.print_text(text, self.settings.HIGHSCORE_TEXT_POS+(0,y_offset), \
                    self.settings.DEMIBOLD_BIG,\
                    self.settings.BLUE,\
                    )
            i += 1
        if self.entering:
            self.frame.print_text("High Score! Please enter your name:",\
                    self.settings.HIGHSCORE_TEXT_POS+(0,y_offset+50),\
                    self.settings.DEMIBOLD_BIG,self.settings.BLUE
                    )
            self.frame.print_text(self.entered_name,\
                    self.settings.HIGHSCORE_TEXT_POS+(0,y_offset+80),\
                    self.settings.DEMIBOLD_BIG,self.settings.BLUE
                    )

    def enter_score(self,score):
        """
        If the given score fits into the list,
        a name will be requested.
        """
        if self.highscores.is_in_highscores(score):
            self.entered_score = score
            self.entered_name = ''

    @property
    def entering(self):
        return self.entered_score > 0

    def update(self):
        self.draw()
        pygame.display.update()

    def activate(self):
        self.egen.add_updateable(self)
        # add new score
        if self.entering:
            elis = TextEnteringListener(self, self.settings)
            self.egen.add_listener(elis)
            self.egen.event_loop()
            self.egen.remove_listener(elis)
            self.highscores.insert_entry(self.entered_name, self.entered_score)
        # display highscores and wait for a key
        elis = AnyKeyListener()
        self.egen.add_listener(elis)
        self.egen.event_loop()
        self.egen.remove_listener(elis)
        self.egen.remove_updateable(self)


