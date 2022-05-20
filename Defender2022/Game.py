from constants import GameConstants, Colors
from Sprites import Player, Enemy, Projectile
from Widgets import Paragraph, TableWidget, PlayButton, ScoreWidget, SideScroller, InputBox
from pygame import init, display, time, event, key, USEREVENT
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

    def event_handler(self, e: event.Event, **kwargs) -> None:
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
            self.add_sprite_to_game(Enemy)
        elif e.type == self.MOUSEBUTTONDOWN and self.MAIN_MENU_ACTIVE and kwargs["play_button"].is_over():
            self.continue_to_main_game()
        if e.type == self.KEYUP and e.key in (self.K_LEFT, self.K_RIGHT) and self.GAME_RUNNING:
            player = kwargs["player"]
            player.accel_x = 0
        if e.type == self.KEYDOWN and e.key == self.K_SPACE and self.GAME_RUNNING:
            player = kwargs['player']
            x = player.rect[0]
            y = player.rect[1]
            if player.forward:
                x += 30
                y += 20
            rect = player.rect.copy()
            forward = player.forward
            self.add_sprite_to_game(Projectile, coordinates=(x, y), forward=forward, rect=rect)
        if e.type == self.MOVE_TIME and self.GAME_RUNNING:
            kwargs["score_widget"].update_time()

    def add_sprite_to_game(self, class_object: type, coordinates: tuple or None = None, **kwargs) -> None or type:
        """
        This method receives the Player or Enemy, the initializes it. After that it is added to our
        Game class's python dictionary, a corresponding pygame Group, then finally the ALL_GROUP pygame group
        :param class_object: the Player, or Enemy, or any Sprite class.
        :param coordinates: a tuple of coordinates can be defined at this level if not the default
        is the center of the screen
        :return: void
        """
        if not kwargs:
            screen_object = class_object()
        else:
            screen_object = class_object(**kwargs)
        if not coordinates:
            coordinates = (self.SCREEN_WIDTH / 100 * 50, self.SCREEN_HEIGHT * 2 / 100 * 50)
        self.SCREEN.blit(screen_object.surf, coordinates)
        if type(screen_object) == Player:
            self.PLAYER_GROUP.add(screen_object)
            self.ALL_GROUP.add(screen_object)
            return screen_object
        elif type(screen_object) == Enemy:
            self.ENEMY_GROUP.add(screen_object)
        elif type(screen_object) == Projectile:
            self.PROJECTILE_GROUP.add(screen_object)
        self.ALL_GROUP.add(screen_object)

    def update_game(self, pressed_keys: tuple or bool, **kwargs) -> None:
        """
        This method calls the player class's updated method with the parameter pressed_keys,
        calls the update  method for the ENEMY sprite group, fills the screen, calls the blit method
        for every single sprite, and flips the display to bring them to the front
        :param pressed_keys:
        :return:
        """
        collided = None
        self.PLAYER_GROUP.update(pressed_keys)
        self.ENEMY_GROUP.update()
        self.PROJECTILE_GROUP.update()
        for entity in self.ALL_GROUP:
            self.SCREEN.blit(entity.surf, entity.rect)

        for enemy in self.ENEMY_GROUP:
            if spritecollide(enemy, self.PROJECTILE_GROUP, False):
                kwargs['score_widget'].update_score()
                collided = enemy

        for projectile in self.PROJECTILE_GROUP:
            if spritecollide(projectile, self.ENEMY_GROUP, False):
                projectile.kill()
                collided.kill()
        if "player" in kwargs and spritecollideany(kwargs["player"], self.ENEMY_GROUP):  # todo make this a class method
            kwargs["player"].kill()
            self.GAME_RUNNING = False

    def menu(self) -> None:
        """
        This method runs the menu screen
        :return: void
        """
        display.set_caption("Main Menu")
        tw = TableWidget(25, 5, 50, 50, data=self.db.get_scores(), columns=("Name", "Score", "Time"))
        title = Paragraph(25, 70, 50, 10, text="Press Space to shoot and use arrow keys to move\nPress ESC to quit")
        play_button = PlayButton(45, 90, 10, 10)
        while self.MAIN_MENU_ACTIVE:
            for e in event.get():
                self.event_handler(e, play_button=play_button)
            self.SCREEN.blit(self.MENU_IMAGE, (0, 0))
            if play_button.is_over():
                play_button.add(self.SCREEN, self.LIGHTER)
            else:
                play_button.add(self.SCREEN, self.DARKER)
            tw.add(self.SCREEN, self.RED)
            title.add(self.SCREEN, self.LIGHTER)
            display.flip()

    def main_game(self):
        """
        This method runs the main game
        :return: void
        """
        time.set_timer(self.ADD_ENEMY, 1000)  # timer manages event triggers
        display.set_caption("Defender 2022!")
        player = self.add_sprite_to_game(Player)
        sw = ScoreWidget(100, 20, 1, 1)
        ss = SideScroller(300, 100, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        time.set_timer(self.MOVE_TIME, 1000)
        while self.GAME_RUNNING:
            ss.add(self.SCREEN)
            ss.slide()
            for e in event.get(): # this event handler
                self.event_handler(e, score_widget=sw, player=player)
            player.x_change += player.accel_x
            if abs(player.x_change) >= player.max_speed:
                player.x_change = player.x_change/abs(player.x_change) * player.max_speed
            if player.accel_x == 0:
                player.x_change *= 0.92
            sw.show(self.SCREEN)
            self.update_game(key.get_pressed(), score_widget=sw, player=player)
            display.flip()
            self.clock.tick(60)
        self.continue_to_final_menu()
        return sw.final_score()

    def final_menu(self, score, time_score):
        display.set_caption("Thanks For Playing!")
        title_txt = f"Thanks For Playing!\n\nPlease Enter Your Name Below\n\nScore: {score}\n\nTime: {time_score}"
        title = Paragraph(30, 5, 400, 400, text=title_txt)
        txt = InputBox(45, 45, 100, 2)
        while self.FINAL_MENU_ACTIVE:
            for e in event.get():
                self.event_handler(e)
                if e.type == self.MOUSEBUTTONDOWN and txt.collidepoint(e.pos):
                    txt.set_active_status(active=True)
                elif e.type == self.MOUSEBUTTONDOWN and not txt.collidepoint(e.pos):
                    txt.set_active_status(active=False)
                if e.type == self.KEYDOWN and e.key == self.K_BACKSPACE and txt.active:
                    txt.user_text = txt.user_text[:-1]
                elif e.type == self.KEYDOWN and e.key != self.K_BACKSPACE and txt.active:
                    txt.user_text += e.unicode
                if e.type == self.KEYDOWN and e.key == self.K_RETURN and txt.user_text != "":
                    name = txt.user_text
                    self.db.add_high_score(name, score, time_score)
                    self.reset_game()
            self.SCREEN.blit(self.FINAL_MENU_IMAGE, (0, 0))
            title.add(self.SCREEN, Colors.ORANGE)
            txt.add(self.SCREEN, txt.color)
            display.flip()
            self.clock.tick(60)
        self.reset_groups()
        self.run()

    def reset_groups(self):
        self.ALL_GROUP = Group()
        self.ENEMY_GROUP = Group()
        self.PLAYER_GROUP = Group()
        self.PROJECTILE_GROUP = Group()

    def run(self):
        self.menu()
        self.GAME_RUNNING = True
        score, time_score = self.main_game()
        self.final_menu(score, time_score)
