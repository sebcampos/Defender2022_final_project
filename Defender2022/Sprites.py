import random
from os.path import sep
from constants import GameConstants, Colors
from pygame import image, transform
from pygame.sprite import Sprite
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class DefenderSprite(GameConstants, Sprite, Colors):
    """
    This Class inherits Constants for our game as well as the Sprite Class
    To build Our Sprites
    """


class Player(DefenderSprite):
    """
    This Class From the Custom Sprite class is used to build the game player
    """
    def __init__(self) -> None:
        super().__init__()
        self.x = self.SCREEN_WIDTH / 100 * 5
        self.y = self.x / 3
        self.surf = image.load("assets" + sep + "spaceship.PNG").convert()
        self.surf.set_colorkey(self.WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (self.x, self.y))
        self.rect = self.surf.get_rect()
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
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 6)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if self.forward:
                self.surf = transform.flip(self.surf, True, False)
            self.forward = False
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if not self.forward:
                self.surf = transform.flip(self.surf, True, False)
            self.forward = True

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT


class Enemy(DefenderSprite):
    """
    This class is used to randomly generate enemy sprites along the x and y axis
    with a random velocity and direction
    """
    def __init__(self):
        super().__init__()
        self.x = self.SCREEN_WIDTH / 100 * 2
        self.y = self.x
        self.surf = image.load("assets" + sep + "enemy.PNG").convert()
        self.surf.set_colorkey(self.WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (self.x, self.y))
        self.forward = random.choice([True, False])
        self.upward = random.choice([True, False])
        self.axis = random.choice(["x", "y"])
        if self.forward and self.axis == "x":
            center = (
                -20,
                random.randint(0, self.SCREEN_HEIGHT),
            )
        elif not self.forward and self.axis == "x":
            center = (
                random.randint(self.SCREEN_WIDTH + 20, self.SCREEN_WIDTH + 100),
                random.randint(0, self.SCREEN_HEIGHT),
            )
        elif self.upward and self.axis == "y":
            center = (
                random.randint(0, self.SCREEN_WIDTH),
                -20,
            )
        elif not self.upward and self.axis == "y":
            center = (
                random.randint(0, self.SCREEN_WIDTH),
                random.randint(self.SCREEN_WIDTH + 20, self.SCREEN_WIDTH + 100),
            )
        self.rect = self.surf.get_rect(
            center=center
        )
        self.speed = random.randint(1, 5)

    def update(self):
        """
        This method moves the Enemy instance up or down the x or y axis
        at the speed of the instance `speed` attribute
        :return: void
        """
        if self.forward and self.axis == "x":
            self.rect.move_ip(+self.speed, 0)
        elif not self.forward and self.axis == "x":
            self.rect.move_ip(-self.speed, 0)
        elif self.upward and self.axis == "y":
            self.rect.move_ip(0, +self.speed)
        elif not self.upward and self.axis == "y":
            self.rect.move_ip(0, -self.speed)
        if self.rect.right < 0 and not self.forward and self.axis == "x":
            self.kill()
        elif self.rect.left > self.SCREEN_WIDTH and self.forward and self.axis == "x":
            self.kill()
        # elif self.rect.top+20 > self.SCREEN_HEIGHT and not self.upward and self.axis == "y":
        #     self.kill()
        elif self.rect.bottom < -20 and self.upward and self.axis == "y":
            self.kill()


class Projectile(DefenderSprite):
    """
    This Class represents the projectile that will be shot from the Player isntance's
    position
    """
    def __init__(self, forward, rect):
        super().__init__()
        self.forward = forward
        self.surf = image.load("assets" + sep + "projectile.PNG").convert()
        self.surf.set_colorkey(self.WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (self.SCREEN_WIDTH / 100 * 3, 10))
        self.rect = rect
        self.speed = 50  # random.randint(50, 80)
        if not forward:
            self.surf = transform.flip(self.surf, True, False)

    def update(self):
        """
        This method moves the projectile defined by the speed attribute forward or backwards along the x axis
        :return: void
        """
        if self.forward:
            self.rect.move_ip(+self.speed, 0)
        elif not self.forward:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > self.SCREEN_WIDTH:
            self.kill()
