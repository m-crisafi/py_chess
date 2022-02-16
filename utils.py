import pygame
from configs import configs

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


def split_image(filename) -> []:
    """
    Splits the passed chess tilemap into 2 rows and 6 columns
    EXPECTED: K Q B N R P
              k q b n r p
    :param filename: the given filename
    :return [images]:
    """
    result = {}

    img = pygame.image.load("assets/%s" % filename)
    img = pygame.transform.scale(
        img,
        (6 * configs["cell_size"],
         2 * configs["cell_size"]))

    for y in range(2):
        color = configs["player_tags"][y]
        result[color] = []

        for x in range(6):
            image = img.subsurface(
                x * configs["cell_size"],
                y * configs["cell_size"],
                configs["cell_size"],
                configs["cell_size"])
            result[color].append(image)

    return result


def load_and_scale(filename):
    """
    Loads and scales the passed board image to the calculated board size
    :param filename: the given filename
    :return: image
    """
    img = pygame.image.load("assets/%s" % filename)
    img = pygame.transform.scale(
        img,
        (configs["board_size"] * configs["cell_size"],
         configs["board_size"] * configs["cell_size"]))
    return img


def idx_to_letter(value) -> str:
    """
    Returns the letter corresponding to the given index
    :param value:
    :return: string
    """
    return LETTERS[value]


def coord_to_notation(coord: (int, int)) -> str:
    """
    Transforms a board coordinate into a chess notation sting, eg. E4
    :param coord: the passed board index
    :return: string
    """
    return idx_to_letter(coord[0]) + str(coord[1] + 1)


def invert_team_color(value: str) -> str:
    """
    Inverts the passed team color
    :param value: the current turn
    :return: str
    """
    if value == "white":
        return "black"
    else:
        return "white"
