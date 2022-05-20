from pygame import init, quit, display, image, transform, FULLSCREEN
from os.path import sep
from DB import DatabaseManager
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
    K_SPACE,
    K_BACKSPACE,
    K_RETURN,
    KEYUP
)


class Colors:
    WHITE = (255, 255, 255)
    LIGHTER = (170, 170, 170)
    DARKER = (100, 100, 100)
    ORANGE = ('orange')
    RED = (255, 0, 0)


init()


class GameConstants:
    display_info = display.Info()
    SCREEN_WIDTH = display_info.current_w
    SCREEN_HEIGHT = display_info.current_h
    db = DatabaseManager.init()
    SCORE_MENU = None
    MAIN_MENU_ACTIVE = True
    GAME_RUNNING = False
    FINAL_MENU_ACTIVE = False
    SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
    RLEACCEL = RLEACCEL
    K_UP = K_UP
    K_DOWN = K_DOWN
    K_LEFT = K_LEFT
    K_RIGHT = K_RIGHT
    K_ESCAPE = K_ESCAPE
    KEYDOWN = KEYDOWN
    QUIT = QUIT
    MOUSEBUTTONDOWN = MOUSEBUTTONDOWN
    K_SPACE = K_SPACE
    K_BACKSPACE = K_BACKSPACE
    K_RETURN = K_RETURN
    KEYUP = KEYUP
    MENU_IMAGE = transform.scale(image.load("assets"+sep+"Level1.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

    @classmethod
    def continue_to_main_game(cls):
        cls.GAME_RUNNING = True
        cls.MAIN_MENU_ACTIVE = False

    @classmethod
    def continue_to_final_menu(cls):
        cls.GAME_RUNNING = False
        cls.FINAL_MENU_ACTIVE = True

    @classmethod
    def reset_screen(cls):
        cls.SCREEN = display.set_mode((cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT), FULLSCREEN)

    @classmethod
    def reset_game(cls):
        cls.GAME_RUNNING = False
        cls.FINAL_MENU_ACTIVE = False
        cls.MAIN_MENU_ACTIVE = True

    @classmethod
    def quit(cls):
        cls.reset_game()
        exit()


quit()
