import utils
from config import configs
from models.piece import Piece

WHITE_IDX = 0
BLACK_IDX = 1

KING_IDX = 0
QUEEN_IDX = 1
BISHOP_IDX = 2
KNIGHT_IDX = 3
ROOK_IDX = 4
PAWN_IDX = 5

DEFAULT_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Factory:

    @staticmethod
    def create_board(images, fe_notation=DEFAULT_START):
        pieces = [[None for x in range(configs["board_size"])] for y in range(configs["board_size"])]
        x = 0
        y = 0

        for char in fe_notation:
            n_piece = None

            if char == "/":
                y += 1
                x = 0
                continue
            elif char.isnumeric():
                x += int(char)
                continue
            elif char == "r":
                n_piece = Piece("rook", images["black"][ROOK_IDX], "black")
            elif char == "R":
                n_piece = Piece("rook", images["white"][ROOK_IDX], "white")
            elif char == "n":
                n_piece = Piece("knight", images["black"][KNIGHT_IDX], "black")
            elif char == "N":
                n_piece = Piece("knight", images["white"][KNIGHT_IDX], "white")
            elif char == "b":
                n_piece = Piece("bishop", images["black"][BISHOP_IDX], "black")
            elif char == "B":
                n_piece = Piece("bishop", images["white"][BISHOP_IDX], "white")
            elif char == "k":
                n_piece = Piece("king", images["black"][KING_IDX], "black")
            elif char == "K":
                n_piece = Piece("king", images["white"][KING_IDX], "white")
            elif char == "q":
                n_piece = Piece("queen", images["black"][QUEEN_IDX], "black")
            elif char == "Q":
                n_piece = Piece("queen", images["white"][QUEEN_IDX], "white")
            elif char == "p":
                n_piece = Piece("pawn", images["black"][PAWN_IDX], "black")
            elif char == "P":
                n_piece = Piece("pawn", images["white"][PAWN_IDX], "white")

            pieces[y][x] = n_piece
            x += 1
            if x >= configs["board_size"]:
                x = 0

        return pieces
