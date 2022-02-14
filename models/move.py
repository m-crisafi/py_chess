import utils
import copy
from configs import configs
from models.chess import Chess
from models.piece import Piece


class Move:

    def __init__(self,
                 chess: Chess):
        """
        Initalises the move checking object with the game object
        :param chess: pointer to the current chess object
        """
        self.chess = chess
        self.piece_moves = []

        self.current_moves = {
            "white": [],
            "black": [],
        }

    def moves_for_color(self,
                        color: str) -> (str, [(int, int)]):
        """
        Returns the current moves for the given piece
        :param color: the given color
        :return: (str, [(int, int)])
        """
        return "team", self.current_moves[color]

    def moves_for_piece(self,
                        piece: Piece) -> (str, [(int, int)]):
        """
        Returns all moves for the given piece
        :param piece: the given piece
        :return: (str, [(int, int)])
        """
        for value in self.piece_moves:
            if value[0] == piece.id:
                return "piece", value[1]

    def can_move(self,
                 piece: Piece,
                 coord: (int, int)) -> bool:
        """
        Checks a given piece can move to a given coordinate
        :param piece: the given piece
        :param coord: the given coordinate
        :return: bool
        """
        opponents_color = utils.invert_team_color(piece.color)

        # check if king can move but not move into check
        if piece.key == "king":
            return utils.list_contains(self.current_moves[opponents_color], (coord[0], coord[1]))

        # check all other pieces, its assumed here the given piece is picked up
        else:
            for value in self.piece_moves:
                if value[0] == piece.id:
                    if utils.list_contains(value[1], coord):
                        # if we can move to the position, recalculate and test for check
                        self.chess.put_down(coord[0], coord[1])
                        new_moves = self.__recalculate_for_color(opponents_color)
                        king = self.chess.get_king(piece.color)
                        coords = self.chess.piece_idx(king)
                        result = utils.list_contains(new_moves, coords)
                        # pickup the piece again to let the main game loop handle the put down
                        self.chess.pickup(coord[0], coord[1])
                        return not result
            return False

    def update(self) -> None:
        """
        Updates all lists of available moves
        :return: None
        """
        self.current_moves["white"] = []
        self.current_moves["black"] = []
        self.piece_moves = []

        for piece in self.chess.pieces:
            moves = self.__check_moves_for_piece(piece)
            self.current_moves[piece.color].extend(moves)
            self.piece_moves.append((piece.id, moves))

    def __recalculate_for_color(self,
                                color) -> [(int, int)]:
        """
        Returns a new array with all the given colors moves.
        :param color: the given color
        :return: [(int, int]
        """
        result = []
        for piece in self.chess.pieces:
            if piece.color == color:
                result.extend(self.__check_moves_for_piece(piece))
        return result

    def __check_moves_for_piece(self,
                                piece: Piece) -> [(int, int)]:
        """
        Checks all possible moves for a given piece
        :param piece: the given piece
        :return: [(x, y)]
        """
        result = []
        # check the type of each piece and call the appropriate function
        if piece.key == "bishop":
            result.extend(self.__bishop(piece))
        elif piece.key == "rook":
            result.extend(self.__rook(piece))
        elif piece.key == "knight":
            result.extend(self.__knight(piece))
        elif piece.key == "queen":
            result.extend(self.__queen(piece))
        elif piece.key == "king":
            result.extend(self.__king(piece))
        elif piece.key == "pawn":
            result.extend(self.__pawn(piece))

        return result

    def __bishop(self,
                 piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given bishop
        :param piece: the given piece
        :return: [(x, y)]
        """
        return self.__trace_diagonals(piece)

    def __rook(self,
               piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given rook
        :param piece: the given piece
        :return: [(x, y)]
        """
        return self.__trace_vertical_horizontal(piece)

    def __knight(self,
                 piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given knight
        :param piece: the given piece
        :return: [(x, y)]
        """
        result = []
        coords = self.chess.piece_idx(piece)
        # up left / up right / down left / down right / left up / left down / right up / right down
        result.extend(self.__check_relative_to_piece(piece, -1, -2))
        result.extend(self.__check_relative_to_piece(piece, 1, -2))
        result.extend(self.__check_relative_to_piece(piece, -1, 2))
        result.extend(self.__check_relative_to_piece(piece, 1, 2))
        result.extend(self.__check_relative_to_piece(piece, -2, -1))
        result.extend(self.__check_relative_to_piece(piece, -2, 1))
        result.extend(self.__check_relative_to_piece(piece, 2, 1))
        result.extend(self.__check_relative_to_piece(piece, 2, -1))
        return result

    def __queen(self,
                piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given queen
        :param piece: the given piece
        :return: [(x, y)]
        """
        result = []
        result.extend(self.__trace_diagonals(piece))
        result.extend(self.__trace_vertical_horizontal(piece))
        return result

    def __king(self,
               piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given king
        :param piece: the given piece
        :return: [(x, y)]
        """
        result = []
        result.extend(self.__trace_diagonals(piece, count=1))
        result.extend(self.__trace_vertical_horizontal(piece, count=1))
        result.extend(self.__check_castling(piece, -1))
        result.extend(self.__check_castling(piece, 1))
        return result

    def __pawn(self,
               piece: Piece) -> [(int, int)]:
        """
        Returns all moves for the given black pawn
        :param piece: the given piece
        :return: [(x, y)]
        """
        result = []
        y_inc = -1

        if piece.color == "black":
            y_inc = 1

        # check if the pawn can make the double starting move
        if not piece.has_moved:
            count = 2
        else:
            count = 1

        result.extend(self.__trace(piece, 0, y_inc, count=count, take_pieces=False))

        # check left and right diagonals
        for i in range(-1, 2, 2):
            c = self.chess.piece_idx(piece)
            x = c[0] + i
            y = c[1] + y_inc

            if Move.coord_in_range(x) and Move.coord_in_range(y):
                n_piece = self.chess.board[y][x]
                if n_piece and (n_piece.color != piece.color):
                    result.append((x, y))

        return result

    def __check_castling(self,
                         king: Piece,
                         inc: int) -> [(int, int)]:
        """
        Checks if the king can make a castling move in the given direction
        :param king: the given king
        :param inc: -1 or 1 for left and right
        :return: [(int, int)]
        """
        result = []

        if not king.has_moved:
            coords = self.chess.piece_idx(king)
            for x in range(1, configs["board_size"]):
                if self.coord_in_range(x):
                    n_piece = self.chess.board[coords[1]][coords[0] + (inc * x)]
                    if not n_piece:
                        continue
                    if n_piece.color == king.color and \
                       n_piece.key == "rook" and \
                       not n_piece.has_moved:
                        if self.__check_is_in_check(king, (coords[0] + inc)) and \
                           self.__check_is_in_check(king, (coords[0] + (inc * 2))):
                            result.append((coords[0] + inc, coords[1]))
                        break
                    else:
                        break

        return result

    def __trace_diagonals(self,
                          piece: Piece,
                          count: int = configs["board_size"]) -> [(int, int)]:
        """
        Traces all diagonals from the given piece
        :param piece: the given piece
        :param count: how far to count from the given piece
        :return:
        """
        result = []
        # top left / top right / bottom left / bottom right
        result.extend(self.__trace(piece, -1, -1, count))
        result.extend(self.__trace(piece, 1, -1, count))
        result.extend(self.__trace(piece, -1, 1, count))
        result.extend(self.__trace(piece, 1, 1, count))
        return result

    def __trace_vertical_horizontal(self,
                                    piece: Piece,
                                    count: int = configs["board_size"]) -> [(int, int)]:
        """
        Traces all vertical and horizontal lines from the given piece
        :param piece: the given piece
        :param count: how far to count from the given piece
        :return:
        """
        result = []
        # up / down / left / right
        result.extend(self.__trace(piece, 0, -1, count))
        result.extend(self.__trace(piece, 0, 1, count))
        result.extend(self.__trace(piece, -1, 0, count))
        result.extend(self.__trace(piece, 1, 0, count))
        return result

    def __trace(self,
                piece: Piece,
                x_inc: int,
                y_inc: int,
                count: int,
                take_pieces: bool = True) -> [(int, int)]:
        """
        Traces along the x, y plane from the given piece until it hits the count or another piece
        :param piece: the given piece
        :param x_inc: the increment direction on the x plane
        :param y_inc: the increment direction on the y plane
        :param count: how far to count from the given piece
        :param take_pieces: take any opposing colours pieces
        :return: [(x, y)]
        """
        result = []
        coords = self.chess.piece_idx(piece)
        x = coords[0]
        y = coords[1]
        step = 0

        while step != count:
            x += x_inc
            y += y_inc
            if Move.coord_in_range(x) and Move.coord_in_range(y):
                n_piece = self.chess.board[y][x]
                if n_piece:
                    if (n_piece.color != piece.color) and take_pieces:
                        result.append((x, y))
                        return result
                    else:
                        return result
                else:
                    result.append((x, y))
            else:
                return result
            step += 1

        return result

    def __check_relative_to_piece(self,
                                  piece: Piece,
                                  x_inc: int,
                                  y_inc: int) -> (int, int):
        """
        Checks if piece can move to the coordinate x_inc and y_inc from the give piece
        :param piece:
        :param x_inc:
        :param y_inc:
        :return: (int, int)
        """
        result = []
        coords = self.chess.piece_idx(piece)
        x = coords[0] + x_inc
        y = coords[1] + y_inc

        if Move.coord_in_range(x) and Move.coord_in_range(y):
            n_piece = self.chess.board[y][x]

            if not n_piece or (n_piece and n_piece.color != piece.color):
                result.append((x, y))
                return result

        return result

    @staticmethod
    def coord_in_range(coord: int) -> bool:
        """
        Checks if the given coordinate value is in bounds of the screen
        :param coord:
        :return: boolean
        """
        return 0 <= coord < configs["board_size"]
    
    @staticmethod
    def coords_int_range(x: int,
                         y: int) -> bool:
        """
        Checks if the given coordinate is in bounds of the screen
        :param x: the given x value
        :param y: the given y value
        :return: boolean
        """
        return Move.coord_in_range(x) and Move.coord_in_range(y)