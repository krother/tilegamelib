
from tilegamelib.basic_boxes import ImageBox
from tilegamelib.frame import Frame
from tilegamelib.events import EventGenerator
from tilegamelib.vector import Vector
from tilegamelib.event_listener import TextEnteringListener, AnyKeyListener
import pygame
from tilegamelib.util import DEMIBOLD_BIG, BLUE


class HighscoreList:
    """Model for the highscores."""
    def __init__(self, filename, length=10):
        self.filename = filename
        self.length = length
        self.scores = []
        self.load_scores()

    def load_scores(self):
        self.scores = []
        for line in open(self.filename):
            score,name = line.strip().split()
            self.scores.append((int(score), name))

    def write_scores(self):
        out = []
        for score,name in self.scores:
            out.append('%i\t%s\n'%(score, name))
        open(self.filename,'w').writelines(out)

    def is_in_highscores(self, score):
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


class HighscoreBox:
    """
    View for high scores.
    This class manages entering names
    and storing the high scores in a file.
    """
    def __init__(self, frame, egen, highscores, highscore_image, textpos):
        """
        frame - Frame instance
        egen - EventGenerator instance
        """
        self.frame = frame
        self.egen = egen
        self.textpos = textpos
        self.highscores = highscores
        self.image = ImageBox(frame, highscore_image)
        
        # for entering new entries
        self.entering = False
        self.name = ""
        self.score = 0

    def draw(self):
        """Draws the highscore list."""
        self.image.draw()
        i = 0
        for score,name in self.highscores.scores:
            y_offset = i * 30
            text = "%8i - %s"%(score, name)
            self.frame.print_text(text, self.textpos+Vector(0,y_offset), \
                    DEMIBOLD_BIG, BLUE,\
                    )
            i += 1
        if self.entering:
            self.frame.print_text("High Score! Please enter your name:",\
                    self.textpos+Vector(0,y_offset+50), DEMIBOLD_BIG, BLUE)
            self.frame.print_text(self.name,\
                    self.textpos+Vector(0, y_offset+80), DEMIBOLD_BIG, BLUE)

    def enter_score(self, score):
        """
        If the given score fits into the list,
        a name will be requested.
        """
        if self.highscores.is_in_highscores(score):
            self.entering = True
            self.entered_score = score
            self.text = ''

    def entered(self, text):
        self.name = text

    def update(self):
        self.draw()
        pygame.display.update()

    def done(self, text=None):
        self.entering = False
        self.egen.listeners = []

    def activate(self):
        self.egen.add_callback(self)
        if self.entering:
            # add new score
            elis = TextEnteringListener(self.entered, self.done)
            self.egen.add_listener(elis)
            self.egen.event_loop()
            self.highscores.insert_entry(self.name, self.entered_score)
        # display highscores and wait for a key
        elis = AnyKeyListener(self.done)
        self.egen.add_listener(elis)
        self.egen.event_loop()
        self.egen.remove_listener(elis)
        self.egen.remove_callback(self)


def show_highscores(new_score, screen, rect, filename, image, textpos):
    """
    Display high score list and gets a name if the score is high enough.
    """
    screen.clear()
    frame = Frame(screen, rect)
    events = EventGenerator()
    hs = HighscoreList(filename)
    hs = HighscoreBox(frame, events, hs, image, textpos)
    hs.enter_score(new_score)
    hs.activate()
    screen.clear()
    pygame.display.update()

