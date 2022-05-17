import random
from Colors import *
from GameUtils import SideScroller, MouseHandler, ContinueButton, ScoreWidget, TextBox, Title
from pygame import init, display, time, event, key, USEREVENT, FULLSCREEN
from pygame.sprite import spritecollideany, spritecollide
from Database import DatabaseManager
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from pygame.locals import (
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
    ContinueButton.init(SCREEN_WIDTH, SCREEN_HEIGHT)
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
        elif e.type == MOUSEBUTTONDOWN and MouseHandler.clicked_on(ContinueButton.coords, ContinueButton.size):
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
        title_text = "High Scores\n" + scores
        title = Title(cls.SCREEN_WIDTH / 100 * 30, cls.SCREEN_HEIGHT / 100 * 5, 400, 400, text=title_text)
        while cls.menu_active:
            for e in event.get():
                cls.event_handler(e)
            cls.SCREEN.fill(GOLD)
            # if mouse is hovered on a button it
            # changes to lighter shade
            if MouseHandler.hovered_over(ContinueButton.coords, ContinueButton.size):
                ContinueButton.add(cls.SCREEN, LIGHTER)
            else:
                ContinueButton.add(cls.SCREEN, DARKER)
            title.add(cls.SCREEN, GOLD)
            cls.SCREEN.blit(ContinueButton.text, ContinueButton.text_coords)
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
            print(cls.SPRITES)
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
        txt = TextBox(cls.SCREEN_WIDTH / 2, cls.SCREEN_HEIGHT / 2, 200, 100)
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
            title.add(cls.SCREEN, GOLD)
            txt.add(cls.SCREEN, txt.color)
            display.flip()
            cls.clock.tick(60)
        cls.SPRITES = {}
        cls.run()

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
        self.surf = Surface((self.x, self.y))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.parent = None
        self.forward = True
        self.up = False
        self.down = False

    def update(self, pressed_keys: tuple or bool) -> None:
        """
        This method updates the position of the player
        based on the keys pressed
        :param pressed_keys: tuple or bool
        :return: void
        """
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -6)
            self.up = True
            self.down = False
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 6)
            self.down = True
            self.up = False
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.forward = False
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
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
        self.surf = Surface((50, 50))
        self.surf.fill(WHITE)
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
        self.speed = random.randint(10, 15)

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
        self.surf = Surface((10, 10))
        self.surf.fill(WHITE)
        self.rect = rect
        self.speed = random.randint(50, 80)

    def update(self):
        if self.forward:
            self.rect.move_ip(+self.speed, 0)
        elif not self.forward:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > Game.SCREEN_WIDTH:
            self.kill()
