
from tilegamelib.config import config


TEST_DATA_PATH = config.BASE_PATH + '/../test/test_data/'

# title screen
TITLE_IMAGE = TEST_DATA_PATH + 'test_tile.png'
TITLE_RECT = (0, 0, 750, 550)
MENU_KEY_REPEAT = {274: 20, 115: 20}
MENU_RECT = (550, 380, 800, 550)

# game over box
GAME_OVER_IMAGE = TEST_DATA_PATH + 'test_tile.png'

# pause box
PAUSE_IMAGE = TEST_DATA_PATH + 'test_tile.png'
