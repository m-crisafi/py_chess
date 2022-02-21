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

    def __init__(self,
                 images: []):
        self.id = 0
        self.images = images

    def create_board(self,
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
                    n_piece = Piece(self.id, record[1], self.images["white"][record[0]], "white", False)
                    self.id += 1
                    break
                elif record[3] == char:
                    n_piece = Piece(self.id, record[1], self.images["black"][record[0]], "black", False)
                    self.id += 1
                    break

            # set our piece at the given coordinate and increment our x
            pieces[y][x] = n_piece
            x += 1

        # return the generated board
        return pieces

    def generate_promotion_pieces(self,
                                  color: str) -> [Piece]:
        """
        Returns a set of new promotion pieces from the given color
        :param key: the piece's key
        :param color: the given color
        :return: [Piece]
        """
        return [
            Piece(self.id, "queen", self.images[color][1], color, False),
            Piece(self.id, "bishop", self.images[color][2], color, False),
            Piece(self.id, "knight", self.images[color][3], color, False),
            Piece(self.id, "rook", self.images[color][4], color, False)
        ]

    @staticmethod
    def to_fen_string(board: [[Piece]]) -> str:
        """
        Returns a fen string from the given board state
        :param board: the given board
        :return: a formatted fen
        """
        fen = ""

        # iterate the board, count will be used to keep track of how many empty tiles we iterate per row
        for y in range(len(board)):
            count = 0
            for x in range(len(board[0])):
                # get our piece and check if its not null
                piece = board[y][x]
                if piece:
                    # check if we have iterated empty cells and write the value
                    if count > 0:
                        fen += str(count)
                        count = 0
                    # write the character determined by the piece
                    for record in PIECE_INFO:
                        if record[1] == piece.key:
                            if piece.color == "white":
                                fen += record[2]
                            else:
                                fen += record[3]
                else:
                    count += 1
            # check count once more before iterating to the next row
            if count > 0:
                fen += str(count)
            # write the new row char only if we aren't on the final iteration
            if y < len(board) - 1:
                fen += '/'

        print(fen)
        return fen

