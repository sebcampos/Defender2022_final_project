import random
from pygame import init, display, time, USEREVENT, FULLSCREEN
from GameDatabase import DatabaseManager
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Game:
    init()  # calling the pygame init method
    display_info = display.Info()  # getting the current display info
    SCREEN_WIDTH = display_info.current_w  # defining constant width from display info
    SCREEN_HEIGHT = display_info.current_h  # defining constant height from display info
    ADD_ENEMY = USEREVENT + 1  # a user event to create enemies
    SPRITES = {}  # a python dictionary to help track sprites
    ALL_GROUP = Group()  # group to manage coordinates and event between sprites
    PLAYER_GROUP = Group()  # this group will hold the player
    ENEMY_GROUP = Group()  # this group will hold the enemies
    SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
    SCREEN.fill((0, 0, 0))  # background color of the screen
    time.set_timer(ADD_ENEMY, 250)  # timer manages event triggers
    display.set_caption("Defender 2022!")
    db = DatabaseManager.init()
    running = True
    @classmethod
    def add_sprite_to_game(cls, sprite_name: str, class_object: type,
                           coordinates: tuple = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) -> None:
        """
        This method receives the Player or Enemy, the initializes it. After that it is added to our
        Game class's python dictionary, a corresponding pygame Group, then finally the ALL_GROUP pygame group
        :param sprite_name: string value of the unique name for this particular class
        :param class_object: the Player, or Enemy, or any Sprite class.
        :param coordinates: a tuple of coordinates can be defined at this level if not the default
        is the center of the screen
        :return: void
        """
        screen_object = class_object()
        screen_object.parent = cls
        cls.SCREEN.blit(screen_object.surf, coordinates)
        if type(screen_object) == Player:
            cls.SPRITES[sprite_name] = screen_object
            cls.PLAYER_GROUP.add(screen_object)
        elif type(screen_object) == Enemy:
            number = str(len(cls.ENEMY_GROUP))
            cls.SPRITES[sprite_name + number] = screen_object
            cls.ENEMY_GROUP.add(screen_object)
        cls.ALL_GROUP.add(screen_object)

    @classmethod
    def update_sprite(cls, sprite_name: str, pressed_keys: tuple) -> None:
        """
        This method fills the screen <color>, calls the sprite update method by name of sprite and with pressed_keys
        as the argument, the calls the pygame blit method to bring the sprite to the screen
        :param sprite_name: string of the sprite name
        :param pressed_keys: the tuple returned from pygame's get_pressed method
        :return: void
        """
        cls.SCREEN.fill((0, 0, 0))
        cls.SPRITES[sprite_name].update(pressed_keys)
        cls.SCREEN.blit(cls.SPRITES[sprite_name].surf, cls.SPRITES[sprite_name].rect)
        display.flip()

    @classmethod
    def update_game(cls, pressed_keys: tuple) -> None:
        """
        This method calls the player class's updated method with the parameter pressed_keys,
        calls the update  method for the ENEMY sprite group, fills the screen, calls the blit method
        for every single sprite, and flips the display to bring them to the front
        :param pressed_keys:
        :return:
        """
        cls.SPRITES["SpaceShip"].update(pressed_keys)
        cls.ENEMY_GROUP.update()
        cls.SCREEN.fill((0, 0, 0))
        for entity in cls.ALL_GROUP:
            cls.SCREEN.blit(entity.surf, entity.rect)
        display.flip()

    @classmethod
    def event_handler(cls, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cls.running = False
            exit()
        elif event.type == QUIT:
            cls.running = False
            exit()
        elif event.type == cls.ADD_ENEMY:
            cls.add_sprite_to_game("Basic Enemy", Enemy)


class Player(Game, Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.parent = None

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Enemy(Game, Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(self.SCREEN_WIDTH + 20, self.SCREEN_WIDTH + 100),
                random.randint(0, self.SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
