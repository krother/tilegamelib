
from title_screen import TitleScreen
from menu import VERTICAL_MOVES

'''
Game States define flow between title, highscore etc.
'''

class GameState:

    def __init__(self, game_factory, **kwargs):
        self.gf = game_factory
        self.events = self.gf.event_generator
        self.create(**kwargs)
        self.gf.screen.clear()

    def create(self, **kwargs):
        pass
    
    def run(self):
        self.events.add_callback(self)
        self.events.event_loop()
        for elis in self.events.listeners:
            self.events.remove_listener(elis)
        self.events.remove_callback(self)

    def update(self):
        pygame.display.update()

    def get_next_state(self):
        return GameState(self.gf)

#---------------------

class TitleScreenState(GameState):

    def create(self):
        # self.settings.KEY_REPEAT = self.settings.MENU_KEY_REPEAT
        self.title = TitleScreen(self.gf.screen, self.events, self.gf.data['TITLE_RECT'], self.gf.data['TITLE_IMAGE'], [], self.gf.data['MENU_RECT'], VERTICAL_MOVES)
        title.run()
        self.selected = None
        
    def get_next_state(self):
        return self.selected


class GamePausedState(GameState):

    def create(self, paused_state):
        self.paused_state = paused_state
        frame = Frame(self.screen, self.data['PAUSE_BOX_RECT'])
        pause = GamePausedBox(frame, self.data['PAUSE_IMAGE'], 'Game paused - press any key', self.event_generator)
        pause.activate()

    def get_next_state(self):
        return self.paused_state


class GameOverState(GameState):

    def create(self, text, final_score):
        """Displays the game over box for some time."""
        self.final_score = final_score
        frame = Frame(self.screen, self.data['GAME_OVER_RECT'])
        game_over = GameOverBox(frame, self.data['GAME_OVER_IMAGE'], text, \
                    self.data['GAME_OVER_DELAY'], self.data['GAME_OVER_OFFSET'], \
                    self.data['GAME_OVER_COLOR'], DEMIBOLD_BIG)
        game_over.activate()

    def get_next_state(self):
        return HighscoreState(self.gf, self.final_score)


class HighscoreState(GameState):

    def create(self, new_score):
        """
        Display high score list and gets a name if the score is high enough.
        """
        self.screen.clear()
        frame = Frame(self.screen, self.data['HIGHSCORE_RECT'])
        hs = HighscoreList(self.data['HIGHSCORE_FILE'])
        hs = HighscoreBox(frame, self.event_generator, hs, self.data['HIGHSCORE_IMAGE'], self.data['HIGHSCORE_TEXTPOS'])
        hs.enter_score(new_score)
        hs.activate()

    def get_next_state(self):
        return TitleScreenState(self.gf)


def run_game(self, initial_state):
    state = initial_state
    while state:
        state.run()
        state = state.get_next_state()
