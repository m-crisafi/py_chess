import pygame
from configs import configs
from models.piece import Piece

# the row indices of our pieces in the png
WHITE_IDX = 0
BLACK_IDX = 1

"""
Piece construction values
(index into the img array, piece key, white FEN, black FEN)
"""
PIECE_INFO = [
    (0, "king", "K", "k"),
    (1, "queen", "Q", "q"),
    (2, "bishop", "B", "b"),
    (3, "knight", "N", "n"),
    (4, "rook", "R", "r"),
    (5, "pawn", "P", "p")
]


class Factory:

    @staticmethod
    def create_board(images: [],
                     fe_notation: str) -> [[Piece]]:
        """
        Generates a 2D array of pieces from the given FEN string
        :param images: the list of piece pngs
        :param fe_notation: the given FEN string
        :return:
        """
        # created an empty 2D list
        pieces = [[None for x in range(configs["board_size"])] for y in range(configs["board_size"])]
        x = 0
        y = 0
        id = 0

        # iterate our FEN character by character
        for char in fe_notation:
            # reset our next piece
            n_piece = None

            # move to next line if we hit the \
            if char == "/":
                y += 1
                x = 0
                continue

            # increment the x pointer if the character is numeric
            elif char.isnumeric():
                x += int(char)
                continue

            # handle the creation of any pieces
            for record in PIECE_INFO:
                if record[2] == char:
                    n_piece = Piece(id, record[1], images["white"][record[0]], "white", False)
                    id += 1
                    break
                elif record[3] == char:
                    n_piece = Piece(id, record[1], images["black"][record[0]], "black", False)
                    id += 1
                    break

            # set our piece at the given coordinate and increment our x
            pieces[y][x] = n_piece
            x += 1

        # return the generated board
        return pieces
