
from tilegamelib.event_listener import AnyKeyListener, EventListener, TextEnteringListener
from tilegamelib.events import QUIT_EVENT, EventGenerator


COMMANDS = {
    'a': 'Hel',
    'b': 'lo',
    'c': 'World',
    'd': ' '
}


class TestEvent:

    def hel(self):
        self.result += "Hel"

    def lo(self):
        self.result += "lo"

    def world(self):
        self.result += "World"

    def space(self):
        self.result += " "

    def setup(self):
        self.egen = EventGenerator()
        keymap = {
            pygame.K_a: self.hel,
            pygame.K_b: self.lo,
            pygame.K_c: self.world,
            pygame.K_d: self.space
        }
        self.elis = EventListener(keymap)
        self.egen.add_listener(self.elis)
        self.updated = 0
        self.result = ""

    def update(self):
        """Counts how many times the method was called"""
        # callback function called from EventGenerator()
        self.updated += 1

    def test_event_generator(self):
        """Generate some key events and check whether they arrive."""
        self.egen.add_scripted_keys('acb')
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == "HelWorldlo"

    def test_callback(self):
        """Pass scripted keys as a string."""
        self.egen.add_callback(self)
        self.egen.add_scripted_keys('abdc')
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == "Hello World"
        assert self.updated == 5

    def test_scripted_repeat(self):
        """Pass scripted keys as a string."""
        self.egen.add_callback(self)
        self.egen.add_scripted_keys('aaaa')
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.updated == 5


class TestAnyKeyListener:

    def callback(self):
        self.keypressed = True

    def test_anykey_negative(self):
        self.keypressed = False
        self.egen = EventGenerator()
        self.elis = AnyKeyListener(self.callback)
        self.egen.add_listener(self.elis)
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert not self.keypressed

    def test_anykey_positive(self):
        self.keypressed = False
        self.egen = EventGenerator()
        self.elis = AnyKeyListener(self.callback)
        self.egen.add_listener(self.elis)
        self.egen.add_scripted_keys('a')
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.keypressed


class TestTextEnteringListener:
    def setup(self):
        self.egen = EventGenerator()
        self.updated = 0
        self.result = ""

    def text_finished(self, text):
        """Callback for listener."""
        self.result = text

    def key_pressed(self, text):
        """Counts how many times the method was called"""
        self.updated += 1

    def test_text_entering(self):
        """Generate some key events and check whether they arrive."""
        elis = TextEnteringListener(self.key_pressed, self.text_finished)
        self.egen.add_listener(elis)
        self.egen.add_scripted_keys('acbd')
        self.egen.add_scripted_keys(chr(K_RETURN))
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == "ACBD"
        assert self.updated == 4

    def test_return_missing(self):
        """Generate some key events and check whether they arrive."""
        elis = TextEnteringListener(self.key_pressed, self.text_finished)
        self.egen.add_listener(elis)
        self.egen.add_scripted_keys('acbd')
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == ""

    def test_delete(self):
        """Generate some key events and check whether they arrive."""
        elis = TextEnteringListener(self.key_pressed, self.text_finished)
        self.egen.add_listener(elis)
        self.egen.add_scripted_keys('acbd')
        self.egen.add_scripted_keys(chr(K_DELETE))
        self.egen.add_scripted_keys('efg')
        self.egen.add_scripted_keys(chr(K_RETURN))
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == "ACBEFG"
        assert self.updated == 8

    def test_no_upper(self):
        """Generate some key events and check whether they arrive."""
        elis = TextEnteringListener(self.key_pressed, self.text_finished, False)
        self.egen.add_listener(elis)
        self.egen.add_scripted_keys('acbd')
        self.egen.add_scripted_keys(chr(K_RETURN))
        self.egen.add_scripted_event(QUIT_EVENT)
        self.egen.event_loop()
        assert self.result == "acbd"
        assert self.updated == 4
