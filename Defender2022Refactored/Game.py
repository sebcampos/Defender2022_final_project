import random
from constants import GameConstants, Colors
from Sprites import Player, Enemy, Projectile
from Widgets import *
from GameUtils import SideScroller, MouseHandler, PlayButton, ScoreWidget, TextBox, Title, TableWidget
from pygame import init, transform, display, time, event, key, image, USEREVENT, FULLSCREEN
from pygame.sprite import spritecollideany, spritecollide
from pygame.sprite import Group


class Game(GameConstants, Colors):
    ADD_ENEMY = USEREVENT + 1
    MOVE_TIME = USEREVENT + 2
    ALL_GROUP = Group()  # group to manage coordinates and event between sprites
    PLAYER_GROUP = Group()  # this group will hold the player
    ENEMY_GROUP = Group()  # this group will hold the enemies
    PROJECTILE_GROUP = Group()

    def __init__(self):
        init()
        self.reset_screen()
        self.clock = time.Clock()

    def event_handler(self, e: event.Event) -> None:
        """
        This method receives the `Event` type of the pygame lib and handles user input
        :param e: Event type of the pygame lib
        :return: void
        """
        if e.type == self.KEYDOWN and e.key == self.K_ESCAPE:
            self.quit()
        elif e.type == self.QUIT:
            self.quit()
        elif e.type == self.ADD_ENEMY and self.GAME_RUNNING:
            print('x')
            #self.add_sprite_to_game("Basic Enemy", Enemy)
        elif e.type == self.MOUSEBUTTONDOWN and MouseHandler.clicked_on(PlayButton.coords, PlayButton.size):
            self.continue_to_main_game()
        if e.type == self.KEYDOWN and e.key == self.K_SPACE and self.GAME_RUNNING:
            pass
            # x = self.SPRITES["Player"].rect[0]
            # y = self.SPRITES["Player"].rect[1]
            # rect = self.SPRITES["Player"].rect.copy()
            # forward = self.SPRITES["Player"].forward
            # self.add_sprite_to_game("Projectile", Projectile, coordinates=(x, y), args=(forward, rect))
        if e.type == self.MOVE_TIME and self.GAME_RUNNING:
            self.SCORE_MENU.update_time()

    def menu(self) -> None:
        """
        This method runs the menu screen
        :return: void
        """
        display.set_caption("Main Menu")
        scores = self.db.get_scores()
        columns = [("Name", "Score", "Time")]
        x = self.SCREEN_WIDTH / 100 * 30
        y = self.SCREEN_HEIGHT / 100 * 5
        width = self.SCREEN_WIDTH / 2
        height = self.SCREEN_HEIGHT / 2
        tw = TableWidget(x, y, width, height, data=scores, columns=columns)
        title_text = "Press Space to shoot and use arrow keys to move\nPress ESC to quit"
        title = Title(self.SCREEN_WIDTH / 100 * 30, self.SCREEN_HEIGHT / 100 * 70, 100, 100, text=title_text)
        playbtn = PlayButton(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        while self.MAIN_MENU_ACTIVE:
            for e in event.get():
                self.event_handler(e)
            self.SCREEN.fill(self.ORANGE)
            # if mouse is hovered on a button it
            # changes to lighter shade
            if MouseHandler.hovered_over(PlayButton.coords, PlayButton.size):
                PlayButton.add(self.SCREEN, self.LIGHTER)
            else:
                PlayButton.add(self.SCREEN, self.DARKER)
            tw.add(self.SCREEN, self.RED)
            title.add(self.SCREEN, self.LIGHTER)
            self.SCREEN.blit(playbtn.text, playbtn.text_coords)
            display.flip()