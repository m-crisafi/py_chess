import pygame
from configs import configs
from game import Game


def open_window() -> pygame.Surface:
    """
    Opens the game window based on the settings in configs.py
    :return: pygame.Surface
    """
    pygame.display.set_caption('Chess')

    return pygame.display.set_mode(
        # set mode takes an (int, int) tuple as the screen size
        ((configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"]) + configs["output_size"],
         (configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"])),
        depth=32
    )


if __name__ == "__main__":
    # open our window and initialise pygame
    screen = open_window()
    pygame.init()
    game = Game(screen)
    game.run()



