# Import the pygame module
import pygame
from GameFactory import Game, Player, Enemy

game = Game()
game.add_sprite_to_game("SpaceShip", Player)

# Main loop
if __name__ == "__main__":
    while game.running:
        for event in pygame.event.get():
            game.event_handler(event)
        pressed_keys = pygame.key.get_pressed()
        game.update_game(pressed_keys)
