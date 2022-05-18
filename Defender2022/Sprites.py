from constants import GameConstants, Colors
import random
from os.path import sep
from pygame import image, transform
from pygame.sprite import Sprite
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Player(GameConstants, Sprite):
    """
    This class inherits from the pygame Sprite and builds our main player
    on the screen
    """

    def __init__(self) -> None:
        super().__init__()
        self.x = 75
        self.y = 25
        self.surf = image.load("assets" + sep + "spaceship.PNG").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
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


class Enemy(GameConstants, Sprite):
    def __init__(self):
        super().__init__()
        self.surf = image.load("assets" + sep + "enemy.PNG").convert()
        self.surf.set_colorkey(Colors.WHITE, RLEACCEL)
        self.surf = transform.scale(self.surf, (50, 50))
        self.forward = random.choice([True, False])
        if self.forward:
            center = (
                -20,
                random.randint(0, self.SCREEN_HEIGHT),
            )
        elif not self.forward:
            center = (
                random.randint(self.SCREEN_WIDTH + 20, self.SCREEN_WIDTH + 100),
                random.randint(0, self.SCREEN_HEIGHT),
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
        elif self.rect.left > self.SCREEN_WIDTH and self.forward:
            self.kill()


class Projectile(GameConstants, Sprite):
    def __init__(self, forward, rect):
        super().__init__()
        self.forward = forward
        self.surf = image.load("assets" + sep + "projectile.PNG").convert()
        self.surf.set_colorkey(Colors.WHITE, RLEACCEL)
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
        elif self.rect.left > self.SCREEN_WIDTH:
            self.kill()
