
import os


class BasicConfig:

    BASE_PATH = os.path.split(__file__)[0]
    DATA_PATH = os.path.join(BASE_PATH, 'data') + os.sep

    # tiles
    TILE_SET = DATA_PATH + 'tiles.xpm'
    TILE_SPECS = DATA_PATH + 'tiles.conf'

    # fonts
    #FONT_FILE = os.path.join(DATA_PATH, 'LucidaSansDemiBold.ttf')
    #DEMIBOLD_BIG = pygame.font.Font(FONT_FILE, 20)
    #DEMIBOLD_SMALL = pygame.font.Font(FONT_FILE, 14)

    DELAY = 0.01
    SHORT_DELAY = 0.05
    VERY_SHORT_DELAY = 0.02

    # screen
    RESOLUTION = (800, 600)
    TILE_SIZE = 32  # changing this will probably break things
    #FRAME = Rect(64, 64, 320, 320)
    BACKGROUND_IMAGE = DATA_PATH + 'background.png'

    # Sound
    MUTE_SOUND = False

    #MAIN_MENU_RECT = Rect(0, 0, 750, 550)
    MAIN_MENU_IMAGE = DATA_PATH + 'title.png'
    #MAIN_MENU_TEXTPOS = Rect(550, 380, 800, 550)
    # MENU_KEY_REPEAT = {274: 20, 115: 20}

    HIGHSCORES = False
    #HIGHSCORE_RECT = Rect(200, 100, 800, 550)
    HIGHSCORE_IMAGE = DATA_PATH + 'background.png'
    HIGHSCORE_TEXT_POS = (0, 0)

    GAME_OVER_IMAGE = DATA_PATH + 'frame_box.png'
    #GAME_OVER_RECT = Rect(200, 150, 400, 100)
    GAME_OVER_OFFSET = (120, 30)
    GAME_OVER_SHORT_OFFSET = (50, 30)
    #GAME_OVER_RECT = Rect(200, 150, 400, 100)
    GAME_OVER_COLOR = (255, 255, 255, 0)
    GAME_OVER_DELAY = 1000
    GAME_OVER_SOUND = {}

    # pause box
    #PAUSE_BOX_RECT = Rect(200, 150, 400, 100)
    PAUSE_IMAGE = DATA_PATH + '/frame_box.png'
    PAUSE_TEXT = "Game Paused - press any key to continue"

    def read_config(filename):
        '''reads lines from config file into a dictionary.'''
        result = {}
        for line in open(filename):
            if '=' in line:
                name, value = line.split('=')
                result[name.strip()] = eval(value.strip())
        return result


config = BasicConfig()
