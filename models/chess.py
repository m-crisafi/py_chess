from models.piece import Piece
from config import configs
from factory import Factory


class Chess:

    def __init__(self):
        self.board = [[]]
        self.pieces = []
        self.picked_up = None
        self.last_position = None
        self.removed = []

    def load_board(self, images, fe_notation=None):
        if not fe_notation:
            self.board = Factory.create_board(images)
        else:
            self.board = Factory.create_board(images, fe_notation)
        self.get_pieces()

    def get_pieces(self):
        for y in range(configs["height"]):
            for x in range(configs["width"]):
                if self.board[y][x]:
                    self.pieces.append(self.board[y][x])

    def piece_idx(self, piece):
        if piece == self.picked_up:
            return self.last_position
        for y in range(configs["height"]):
            for x in range(configs["width"]):
                if self.board[y][x] == piece:
                    return x, y
        return None

    def put_down(self, x, y):
        move_to = self.board[y][x]

        if move_to and self.picked_up.color != move_to.color:
            self.removed.append(move_to)
            self.pieces.remove(move_to)

        self.board[y][x] = self.picked_up
        self.picked_up = None
        self.last_position = None

    def pickup(self, x, y):
        result = self.board[y][x]
        self.board[y][x] = None
        self.picked_up = result
        self.last_position = (x, y)
        return result

    def return_piece(self):
        self.board[self.last_position[1]][self.last_position[0]] = self.picked_up
        self.picked_up = None
        self.last_position = None
