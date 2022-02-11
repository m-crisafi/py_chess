import pygame
from config import configs

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


def split_image(filename, rows, cols):
    result = {}

    img = pygame.image.load("assets/%s" % filename)
    img = pygame.transform.scale(
        img,
        (rows * configs["cell_size"],
         cols * configs["cell_size"]))

    for y in range(cols):
        color = configs["player_tags"][y]
        result[color] = []

        for x in range(rows):
            image = img.subsurface(
                x * configs["cell_size"],
                y * configs["cell_size"],
                configs["cell_size"],
                configs["cell_size"])
            result[color].append(image)

    return result


def load_and_scale(filename):
    img = pygame.image.load("assets/%s" % filename)
    img = pygame.transform.scale(
        img,
        (configs["board_size"] * configs["cell_size"],
         configs["board_size"] * configs["cell_size"]))
    return img


def idx_to_letter(value):
    return LETTERS[value]
