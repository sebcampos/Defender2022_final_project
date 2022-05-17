import random
from os import path
from Colors import *
from GameUtils import SideScroller, MouseHandler, PlayButton, ScoreWidget, TextBox, Title, TableWidget
from pygame import init, transform, display, time, event, key, image, USEREVENT, FULLSCREEN
from pygame.sprite import spritecollideany, spritecollide
from Database import DatabaseManager
from pygame.sprite import Group, Sprite
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
    K_RETURN
)

accel_x = 0
accel_y = 0

class Game:
    init()  # calling the pygame init method
    display_info = display.Info()  # getting the current display info
    SCREEN_WIDTH = display_info.current_w  # defining constant width from display info
    SCREEN_HEIGHT = display_info.current_h  # defining constant height from display info
    SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
    ADD_ENEMY = USEREVENT + 1  # a user event to create enemies
    MOVE_TIME = USEREVENT + 2
    SPRITES = {}  # a python dictionary to help track sprites
    ALL_GROUP = Group()  # group to manage coordinates and event between sprites
    PLAYER_GROUP = Group()  # this group will hold the player
    ENEMY_GROUP = Group()  # this group will hold the enemies
    PROJECTILE_GROUP = Group()
    PlayButton.init(SCREEN_WIDTH, SCREEN_HEIGHT)
    SideScroller.init(SCREEN_WIDTH, SCREEN_HEIGHT)
    db = DatabaseManager.init()
    SCORE_MENU = None
    menu_active = True
    running = False
    final_menu_active = False
    clock = time.Clock()

    @classmethod
    def add_sprite_to_game(cls, sprite_name: str, class_object: type,
                           coordinates: tuple = (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2), args=False) -> None:
        """
        This method receives the Player or Enemy, the initializes it. After that it is added to our
        Game class's python dictionary, a corresponding pygame Group, then finally the ALL_GROUP pygame group
        :param args:
        :param sprite_name: string value of the unique name for this particular class
        :param class_object: the Player, or Enemy, or any Sprite class.
        :param coordinates: a tuple of coordinates can be defined at this level if not the default
        is the center of the screen
        :return: void
        """
        if not args:
            screen_object = class_object()
        else:
            screen_object = class_object(args[0], args[1])
        screen_object.parent = cls
        cls.SCREEN.blit(screen_object.surf, coordinates)
        if type(screen_object) == Player:
            cls.SPRITES[sprite_name] = screen_object
            cls.PLAYER_GROUP.add(screen_object)
        elif type(screen_object) == Enemy:
            number = str(len(cls.ENEMY_GROUP))
            cls.SPRITES[sprite_name + number] = screen_object
            cls.ENEMY_GROUP.add(screen_object)
        elif type(screen_object) == Projectile:
            number = str(len(cls.PROJECTILE_GROUP))
            cls.SPRITES[sprite_name + number] = screen_object
            cls.PROJECTILE_GROUP.add(screen_object)
        cls.ALL_GROUP.add(screen_object)

    @classmethod
    def update_game(cls, pressed_keys: tuple or bool) -> None:
        """
        This method calls the player class's updated method with the parameter pressed_keys,
        calls the update  method for the ENEMY sprite group, fills the screen, calls the blit method
        for every single sprite, and flips the display to bring them to the front
        :param pressed_keys:
        :return:
        """
        collided = None
        cls.SPRITES["Player"].update(pressed_keys)
        cls.SPRITES["Player"].accelerate(pressed_keys)
        cls.ENEMY_GROUP.update()
        cls.PROJECTILE_GROUP.update()
        for entity in cls.ALL_GROUP:
            cls.SCREEN.blit(entity.surf, entity.rect)

        for enemy in cls.ENEMY_GROUP:
            if spritecollide(enemy, cls.PROJECTILE_GROUP, False):
                cls.SCORE_MENU.update_score()
                collided = enemy

        for projectile in cls.PROJECTILE_GROUP:
            if spritecollide(projectile, cls.ENEMY_GROUP, False):
                projectile.kill()
                collided.kill()

        if spritecollideany(cls.SPRITES["Player"], cls.ENEMY_GROUP):
            cls.SPRITES["Player"].kill()
            cls.running = False
        display.flip()

    @classmethod
    def event_handler(cls, e: event.Event) -> None:
        """
        This method receives the `Event` type of the pygame lib and handles user input
        :param e: Event type of the pygame lib
        :return: void
        """
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            cls.running = False
            cls.final_menu_active = False
            cls.menu_active = False
            exit()
        elif e.type == QUIT:
            cls.running = False
            cls.final_menu_active = False
            cls.menu_active = False
            exit()
        elif e.type == cls.ADD_ENEMY and cls.running:
            cls.add_sprite_to_game("Basic Enemy", Enemy)
        elif e.type == MOUSEBUTTONDOWN and MouseHandler.clicked_on(PlayButton.coords, PlayButton.size):
            cls.menu_active = False
            cls.running = True
        if e.type == KEYDOWN and e.key == K_SPACE and cls.running:
            x = cls.SPRITES["Player"].rect[0]
            y = cls.SPRITES["Player"].rect[1]
            rect = cls.SPRITES["Player"].rect.copy()
            forward = cls.SPRITES["Player"].forward
            cls.add_sprite_to_game("Projectile", Projectile, coordinates=(x, y), args=(forward, rect))
        if e.type == cls.MOVE_TIME and cls.running:
            cls.SCORE_MENU.update_time()

    @classmethod
    def menu(cls) -> None:
        """
        This method runs the menu screen
        :return: void
        """
        display.set_caption("Main Menu")
        scores = cls.db.get_scores()
        columns = [("Name", "Score", "Time")]
        x = cls.SCREEN_WIDTH / 100 * 30
        y = cls.SCREEN_HEIGHT / 100 * 5
        width = cls.SCREEN_WIDTH / 2
        height = cls.SCREEN_HEIGHT / 2
        tw = TableWidget(x, y, width, height, data=scores, columns=columns)
        title_text = "Press Space to shoot and use arrow keys to move\nPress ESC to quit"
        title = Title(cls.SCREEN_WIDTH / 100 * 30, cls.SCREEN_HEIGHT / 100 * 70, 100, 100, text=title_text)
        while cls.menu_active:
            for e in event.get():
                cls.event_handler(e)
            cls.SCREEN.fill(ORANGE)
            # if mouse is hovered on a button it
            # changes to lighter shade
            if MouseHandler.hovered_over(PlayButton.coords, PlayButton.size):
                PlayButton.add(cls.SCREEN, LIGHTER)
            else:
                PlayButton.add(cls.SCREEN, DARKER)
            tw.add(cls.SCREEN, RED)
            title.add(cls.SCREEN, LIGHTER)
            cls.SCREEN.blit(PlayButton.text, PlayButton.text_coords)
            display.flip()

    @classmethod
    def main_game(cls) -> None:
        """
        This method runs the main game
        :return: void
        """
        time.set_timer(cls.ADD_ENEMY, 1 * 1000)  # timer manages event triggers
        display.set_caption("Defender 2022!")
        cls.add_sprite_to_game("Player", Player)
        cls.SCORE_MENU = ScoreWidget(cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT)
        time.set_timer(cls.MOVE_TIME, 1000)
        while cls.running:
            cls.SCREEN.blit(SideScroller.background, (SideScroller.bgx, 0))
            SideScroller.bgx -= 1
            if SideScroller.bgx <= -cls.SCREEN_WIDTH * 2:
                SideScroller.bgx = 0
                level = SideScroller.next_level()
                SideScroller.init(cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT, level=level)
            for e in event.get():
                cls.event_handler(e)
            cls.SCREEN.blit(cls.SCORE_MENU.number, cls.SCORE_MENU.number_coords)
            cls.SCREEN.blit(cls.SCORE_MENU.timer, cls.SCORE_MENU.timer_coords)
            cls.update_game(key.get_pressed())
            cls.clock.tick(60)
        cls.final_menu_active = True

    @classmethod
    def final_menu(cls):
        display.set_caption("Thanks For Playing!")
        score = cls.SCORE_MENU.score
        time_score = cls.SCORE_MENU.time_score
        title_txt = f"Thanks For Playing!\n\nPlease Enter Your Name Below\n\nScore: {score}\n\nTime: {time_score}"
        title = Title(cls.SCREEN_WIDTH / 100 * 30, cls.SCREEN_HEIGHT / 100 * 5, 400, 400, text=title_txt)
        txt = TextBox(cls.SCREEN_WIDTH / 2, cls.SCREEN_HEIGHT / 2, 50, 50)
        while cls.final_menu_active:
            for e in event.get():
                cls.event_handler(e)
                if e.type == MOUSEBUTTONDOWN and txt.collidepoint(e.pos):
                    txt.set_active_status(active=True)
                elif e.type == MOUSEBUTTONDOWN and not txt.collidepoint(e.pos):
                    txt.set_active_status(active=False)

                if e.type == KEYDOWN and e.key == K_BACKSPACE and txt.active:
                    txt.user_text = txt.user_text[:-1]
                elif e.type == KEYDOWN and e.key != K_BACKSPACE and txt.active:
                    txt.user_text += e.unicode
                if e.type == KEYDOWN and e.key == K_RETURN:
                    name = txt.user_text
                    if name != "":
                        cls.db.add_high_score(name, score, time_score)
                    cls.final_menu_active = False
                    cls.menu_active = True
            cls.SCREEN.fill(WHITE)
            title.add(cls.SCREEN, ORANGE)
            txt.add(cls.SCREEN, txt.color)
            display.flip()
            cls.clock.tick(60)
        cls.reset_groups()
        cls.run()

    @classmethod
    def reset_groups(cls):
        cls.SPRITES = {}
        cls.ALL_GROUP = Group()
        cls.ENEMY_GROUP = Group()
        cls.PLAYER_GROUP = Group()
        cls.PROJECTILE_GROUP = Group()

    @classmethod
    def run(cls) -> None:
        """
        This method runs the application in order
        :return: void
        """
        cls.menu()
        cls.main_game()
        cls.final_menu()


class Player(Sprite):
    """
    This class inherits from the pygame Sprite and builds our main player
    on the screen
    """

    def __init__(self) -> None:
        super().__init__()
        self.x = 75
        self.y = 25
        self.surf = image.load("assets" + path.sep + "spaceship.PNG").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = transform.scale(self.surf, (self.x, self.y))
        self.rect = self.surf.get_rect()
        self.parent = None
        self.forward = True
        self.up = False
        self.down = False
        self.x_left_accel = 0
        self.x_right_accel = 0
        self.y_up_accel = 0
        self.y_down_accel = 0

    def accelerate(self, pressed_keys: tuple or bool) -> None:
        """
        This method updates the position of the player
        based on the keys pressed
        :param pressed_keys: tuple or bool
        :return: void
        """

        if not (self.y_down_accel < 0) or not (self.y_up_accel < 0) or not (self.x_left_accel < 0) or not (self.x_right_accel < 0):
            if pressed_keys[K_UP]:
                self.y_up_accel += -0.175
                self.rect.move_ip(0, self.y_up_accel)
                self.up = True
                self.down = False
                self.y_down_accel += -0.215
            if pressed_keys[K_DOWN]:
                self.y_down_accel += 0.175
                self.rect.move_ip(0, self.y_down_accel)
                self.down = True
                self.up = False
                self.y_up_accel += 0.215
            if pressed_keys[K_LEFT]:
                self.x_left_accel += -0.175
                self.rect.move_ip(self.x_left_accel, 0)
                self.forward = False
                self.x_right_accel += -0.215
            if pressed_keys[K_RIGHT]:
                self.x_right_accel += 0.175
                self.rect.move_ip(self.x_right_accel, 0)
                self.forward = True
                self.x_left_accel += 0.215
        elif not (self.y_down_accel or self.y_up_accel or self.x_left_accel or self.x_right_accel) > 0.8:
            if pressed_keys[K_UP]:
                self.y_up_accel += -0.175
                self.rect.move_ip(0, self.y_up_accel)
                self.up = True
                self.down = False
                self.y_down_accel += -0.215
            if pressed_keys[K_DOWN]:
                self.y_down_accel += 0.175
                self.rect.move_ip(0, self.y_down_accel)
                self.down = True
                self.up = False
                self.y_up_accel += 0.215
            if pressed_keys[K_LEFT]:
                self.x_left_accel += -0.175
                self.rect.move_ip(self.x_left_accel, 0)
                self.forward = False
                self.x_right_accel += -0.215
            if pressed_keys[K_RIGHT]:
                self.x_right_accel += 0.175
                self.rect.move_ip(self.x_right_accel, 0)
                self.forward = True
                self.x_left_accel += 0.215

        else:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, self.y_up_accel)
                self.up = True
                self.down = False
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, self.y_down_accel)
                self.down = True
                self.up = False
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(self.x_left_accel, 0)
                self.forward = False
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.x_right_accel, 0)
                self.forward = True
    def update(self, pressed_keys: tuple or bool) -> None:
        """
        This method updates the position of the player
        based on the keys pressed
        :param pressed_keys: tuple or bool
        :return: void
        """

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -6)
            y_speed = -6
            self.rect.move_ip(0, y_speed)
            self.up = True
            self.down = False
        if pressed_keys[K_DOWN]:
            y_speed = 6
            self.rect.move_ip(0, y_speed)
            self.down = True
            self.up = False
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if self.forward:
                self.surf = transform.flip(self.surf, True, False)
            x_speed = -6
            self.rect.move_ip(x_speed, 0)
            self.forward = False
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if not self.forward:
                self.surf = transform.flip(self.surf, True, False)
            x_speed = 6
            self.rect.move_ip(x_speed, 0)
            self.forward = True

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Game.SCREEN_WIDTH:
            self.rect.right = Game.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= Game.SCREEN_HEIGHT:
            self.rect.bottom = Game.SCREEN_HEIGHT


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.surf = image.load("assets" + path.sep + "enemy.PNG").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (50, 50))
        self.forward = random.choice([True, False])
        if self.forward:
            center = (
                -20,
                random.randint(0, Game.SCREEN_HEIGHT),
            )
        elif not self.forward:
            center = (
                random.randint(Game.SCREEN_WIDTH + 20, Game.SCREEN_WIDTH + 100),
                random.randint(0, Game.SCREEN_HEIGHT),
            )
        self.rect = self.surf.get_rect(
            center=center
        )
        self.speed = random.randint(10, 50)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        if self.forward:
            self.rect.move_ip(+self.speed, 0)
        elif not self.forward:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0 and not self.forward:
            self.kill()
        elif self.rect.left > Game.SCREEN_WIDTH and self.forward:
            self.kill()


class Projectile(Sprite):
    def __init__(self, forward, rect):
        super().__init__()
        self.forward = forward
        self.surf = image.load("assets" + path.sep + "projectile.PNG").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (20, 10))
        self.rect = rect
        self.speed = 50  # random.randint(50, 80)
        if not forward:
            self.surf = transform.flip(self.surf, True, False)

    def update(self):
        if self.forward:
            self.rect.move_ip(+self.speed, 0)
        elif not self.forward:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > Game.SCREEN_WIDTH:
            self.kill()
