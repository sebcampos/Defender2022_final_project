# Import the pygame module
import pygame
from GameFactory import Game, Player, Enemy
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Variable to keep the main loop running
running = True


game = Game()
game.add_sprite_to_game("SpaceShip", Player)

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        elif event.type == game.ADD_ENEMY:
            game.add_sprite_to_game("Basic Enemy", Enemy)

    pressed_keys = pygame.key.get_pressed()
    game.update_game(pressed_keys)
