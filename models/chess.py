from models.piece import Piece
from configs import configs
from factory import Factory

DEFAULT_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Chess:

    def __init__(self):
        self.board = [[]]           # 2D list of pieces. None if no piece exists at [y][x]
        self.pieces = []            # list of all pieces of the board
        self.removed = []           # list of all removed pieces
        self.picked_up = None       # the currently picked up piece
        self.last_position = None   # the position of the picked up piece

    def load_board(self,
                   images: [],
                   fe_notation: str = DEFAULT_START) -> None:
        """
        Loads the board from the given FEN
        :param images: list of chess piece images
        :param fe_notation: the given FEN
        :return: None
        """
        # load the board using the factory method
        self.board = Factory.create_board(images, fe_notation)

        # iterate the board and append all pieces to the list
        for y in range(configs["board_size"]):
            for x in range(configs["board_size"]):
                if self.board[y][x]:
                    self.pieces.append(self.board[y][x])

    def piece_idx(self,
                  piece: Piece) -> (int, int):
        """
        Returns the coordinates of the given piece.
        :param piece: the given piece
        :return:
        """
        # check the piece isn't currently picked up
        if piece == self.picked_up:
            return self.last_position
        # iterate the board and find the piece
        for y in range(configs["board_size"]):
            for x in range(configs["board_size"]):
                if self.board[y][x] == piece:
                    return x, y

    def put_down(self,
                 x: int,
                 y: int) -> [(Piece, int, int)]:
        """
        Places the given piece on the board, replacing the piece thats there.
        :param x: the target x position
        :param y: the target y potion
        :return: [(Piece, int int)]
        """
        move_to = self.board[y][x]
        # remove the piece at the coordinate if it exists
        if move_to:
            self.removed.append(move_to)
            self.pieces.remove(move_to)
        # place the piece
        self.board[y][x] = self.picked_up
        self.picked_up.has_moved = True

        # check castling case condition
        if self.picked_up.key == "king":
            # check castled left
            if x < self.last_position[0] - 1:
                rook = self.board[y][0]
                self.board[y][0] = None
                self.board[y][self.last_position[0] - 1] = rook
            # check castled right
            elif x > self.last_position[0] + 1:
                rook = self.board[y][configs["board_size"] - 1]
                self.board[y][configs["board_size"] - 1] = None
                self.board[y][self.last_position[0] + 1] = rook

        result = (self.picked_up, x, y)
        self.picked_up = None
        self.last_position = None
        return result

    def pickup(self,
               x: int,
               y: int) -> Piece:
        """
        Picks up the piece at the given x and y position
        :param x: the target x position
        :param y: the target y potion
        :return: None
        """
        result = self.board[y][x]
        self.board[y][x] = None
        self.picked_up = result
        self.last_position = (x, y)
        return result

    def return_piece(self) -> None:
        """
        Returns the picked up piece to the table
        :return: None
        """
        self.board[self.last_position[1]][self.last_position[0]] = self.picked_up
        self.picked_up = None
        self.last_position = None

    def has_piece_at(self,
                     x: int,
                     y: int) -> bool:
        """
        Checks if a piece exists at the given x and y position
        :param x: the target x position
        :param y: the target y position
        :return: bool
        """
        return self.board[y][x] is not None
