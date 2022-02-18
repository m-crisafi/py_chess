import utils
from models.move import Move
from models.piece import Piece
from configs import configs
from factory import Factory

DEFAULT_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Chess:

    def __init__(self,
                 turn: str = "white"):
        """
        Constructor for the chess object
        :param turn: the loaded turn
        """
        self.board = [[]]           # 2D list of pieces. None if no piece exists at [y][x]
        self.pieces = []            # list of all pieces of the board
        self.removed = []           # list of all removed pieces
        self.picked_up = None       # the currently picked up piece
        self.last_position = None   # the position of the picked up piece
        self.turn = "white"         # the current players turn
        self.history = []           # stores [Move]
        self.white_king = None      # pointer to the white king
        self.black_king = None      # pointer to the black king

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

        # find the two kings and set the pointer
        for piece in self.pieces:
            if piece.key == "king" and piece.color == "white":
                self.white_king = piece
            elif piece.key == "king" and piece.color == "black":
                self.black_king = piece

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
                 y: int) -> bool:
        """
        Places the given piece on the board, replacing the piece thats there.
        :param x: the target x position
        :param y: the target y potion
        :return: bool (if successful)
        """
        move = Move(self.picked_up.id, self.last_position, (x, y), -1)

        if (x, y) == self.last_position:
            self.return_piece()
            return False

        move_to = self.board[y][x]

        # remove the piece at the coordinate if it exists
        if move_to:
            self.removed.append(move_to)
            self.set_piece(None, coord)
            move.took_piece = move_to.piece_id

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
                rook.has_moved = True
            # check castled right
            elif x > self.last_position[0] + 1:
                rook = self.board[y][configs["board_size"] - 1]
                self.board[y][configs["board_size"] - 1] = None
                self.board[y][self.last_position[0] + 1] = rook
                rook.has_moved = True

        # check en passent case condition
        if self.picked_up.key == "pawn":
            if self.picked_up.color == "white":
                coord = (x, y + 1)
                piece = self.piece_at(coord)
                if piece and piece.key == "pawn" and \
                   self.last_move().piece_id == piece.id:
                    self.removed.append(piece)
                    self.set_piece(None, coord)
                    move.took_piece = piece.id
            else:
                coord = (x, y - 1)
                piece = self.piece_at(coord)
                if piece and piece.key == "pawn" and \
                   self.last_move().piece_id == piece.id:
                    self.removed.append(piece)
                    self.set_piece(None, coord)
                    move.took_piece = piece.id

        self.history.append(move)
        self.picked_up = None
        self.last_position = None
        self.next_turn()
        return True

    def pickup(self,
               x: int,
               y: int) -> Piece:
        """
        Picks up the piece at the given x and y position
        :param x: the target x position
        :param y: the target y potion
        :return: None
        """
        self.picked_up = self.board[y][x]
        self.board[y][x] = None
        self.last_position = (x, y)
        return self.picked_up

    def return_piece(self) -> None:
        """
        Returns the picked up piece to the table
        :return: None
        """
        self.set_piece(self.picked_up, self.last_position)
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

    def has_piece_at_coord(self,
                           coord: int) -> bool:
        """
        Overload for has_peice_at(int, int)
        :param coord: the target coordinate
        """
        return self.has_piece_at(coord[0], coord[1])

    def next_turn(self) -> str:
        """
        Moves to the next players turn
        :return: str
        """
        self.turn = utils.invert_team_color(self.turn)
        return self.turn

    def pieces_for_color(self,
                         color: str) -> [Piece]:
        """
        Returns all pieces for the given color that are on the board
        :param color: the given color
        :return: [Piece]
        """
        result = []
        for y in range(configs["board_size"]):
            for x in range(configs["board_size"]):
                piece = self.piece_at((x, y))
                if piece and color == piece.color:
                    result.append(piece)
        return result

    def piece_at(self,
                 coord: (int, int)) -> Piece:
        """
        Returns the piece at the given board index
        :param coord: the given board coordinate
        :return: Piece
        """
        return self.board[coord[1]][coord[0]]

    def piece_for_id(self,
                     piece_id: int) -> Piece:
        """
        Returns a piece with the given id
        :param piece_id: the given id
        :return: Piece
        """
        for piece in self.pieces:
            if piece_id == piece.id:
                return piece

        for piece in self.removed:
            if piece_id == piece.id:
                return piece

    def set_piece(self,
                  piece: Piece,
                  coord: (int, int)) -> None:
        """
        Sets the piece at the given board coordinate
        :param piece: the given piece
        :param coord: the given coord
        :return: None
        """
        self.board[coord[1]][coord[0]] = piece

    def get_king(self,
                 color: str) -> Piece:
        """
        Returns the king for the given color
        :param color: the given color
        :return: Piece
        """
        if color == "white":
            return self.white_king
        else:
            return self.black_king

    def last_move(self) -> Move:
        """
        Returns the last move made
        :return: (Piece, from_coord, to_coord, took_piece)
        """
        if len(self.history) > 0:
            return self.history[-1]
