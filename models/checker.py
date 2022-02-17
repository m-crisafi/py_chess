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
        self.__chess = chess
        # stored as [(piece.id, (x, y)]
        self.__current_moves = []

    def moves_for_team(self) -> (str, [(int, int)]):
        """
        Returns the current moves for the given piece. We return "team" attached
        for the renderer to check configs against
        :return: (str, [(int, int)])
        """
        result = []
        for move in self.__current_moves:
            result.extend(move[1])
        return "team", result

    def moves_for_id(self,
                     piece_id: int) -> (str, [(int, int)]):
        """
        Searches the list of piece moves to find the matching ID
        :param piece_id: the given piece id
        :return: (str, [(int, int)])
        """
        for move in self.__current_moves:
            if piece_id == move[0]:
                return "piece", move[1]
        return "piece", []

    def moves_for_piece(self,
                        piece: Piece) -> (str, [(int, int)]):
        """
        Returns all moves for the given piece. We return "piece" attached for the
        renderer to check configs against
        :param piece: the given piece
        :return: (str, [(int, int)])
        """
        return self.moves_for_id(piece.id)

    def can_move(self,
                 piece: Piece,
                 coord: (int, int)) -> bool:
        """
        Checks a given piece can move to a given coordinate
        :param piece: the given piece
        :param coord: the given coordinate
        :return: bool
        """
        return coord in self.moves_for_piece(piece)[1]

    def update(self) -> None:
        """
        Updates all lists of available moves
        :return: None
        """
        self.__current_moves = []

        for piece in self.__chess.pieces:
            if piece.color == self.__chess.turn:
                temp_moves = []
                moves = self.__check_moves_for_piece(piece)
                # self.__current_moves.append((piece.id, moves))
                for coord in moves:
                    if not self.__check_moves_into_check(piece, coord):
                        temp_moves.append(coord)
                if len(temp_moves) > 0:
                    self.__current_moves.append((piece.id, temp_moves))

    def __recalculate_for_color(self,
                                color) -> [(int, int)]:
        """
        Returns a new list with all the given colors moves.
        :param color: the given color
        :return: [(int, int)]
        """
        result = []
        for piece in self.__chess.pieces_for_color(color):
            result.extend(self.__check_moves_for_piece(piece))
        return result

    def __check_moves_into_check(self,
                                 piece: Piece,
                                 to_coord: [int, int]):
        """
        Checks if the given move will trigger check
        :param piece: the given piece
        :param to_coord: the given coord
        :return: true if in check, false if not
        """
        # place the piece for testing
        temp_piece = self.__chess.piece_at(to_coord)
        from_coord = self.__chess.piece_idx(piece)
        self.__chess.set_piece(piece, to_coord)
        self.__chess.set_piece(None, from_coord)

        # recalculate moves for the opponent color
        opponents_color = utils.invert_team_color(piece.color)
        new_moves = self.__recalculate_for_color(opponents_color)

        # check if the king occupies a potential move
        king = self.__chess.get_king(piece.color)
        coords = self.__chess.piece_idx(king)
        result = coords in new_moves

        # remove the piece we placed
        self.__chess.set_piece(temp_piece, to_coord)
        self.__chess.set_piece(piece, from_coord)
        return result

    def __check_moves_for_piece(self,
                                piece: Piece) -> [(int, int)]:
        """
        Checks all possible moves for a given piece
        :param piece: the given piece
        :return: [(x, y)]
        """
        # check the type of each piece and call the appropriate function
        if piece.key == "bishop":
            return self.__bishop(piece)
        elif piece.key == "rook":
            return self.__rook(piece)
        elif piece.key == "knight":
            return self.__knight(piece)
        elif piece.key == "queen":
            return self.__queen(piece)
        elif piece.key == "king":
            return self.__king(piece)
        elif piece.key == "pawn":
            return self.__pawn(piece)

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
            result.extend(self.__trace(piece, 0, y_inc, count=2, take_pieces=False))
        else:
            result.extend(self.__trace(piece, 0, y_inc, count=1, take_pieces=False))

        # check left and right diagonals
        for i in range(-1, 2, 2):
            c = self.__chess.piece_idx(piece)
            x = c[0] + i
            y = c[1] + y_inc

            if Move.coords_in_range(x, y):
                n_piece = self.__chess.board[y][x]
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
            coords = self.__chess.piece_idx(king)
            for x in range(1, configs["board_size"]):
                if self.coord_in_range(x):
                    n_piece = self.__chess.board[coords[1]][coords[0] + (inc * x)]
                    if not n_piece:
                        continue
                    if n_piece.color == king.color and \
                       n_piece.key == "rook" and \
                       not n_piece.has_moved:
                        if self.__check_moves_into_check(king, (coords[0] + inc)) and \
                           self.__check_moves_into_check(king, (coords[0] + (inc * 2))):
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
        coords = self.__chess.piece_idx(piece)
        x = coords[0]
        y = coords[1]
        step = 0

        if piece.key == "bishop":
            print("HALT")
            print("HALT")

        # loop until we have hit our total count
        while step < count:
            # increment our target x and y positions from the passed incremenets
            x += x_inc
            y += y_inc
            # check our new coordinate is in range
            if Move.coords_in_range(x, y):
                # get the piece at the given position (None if no piece exists)
                n_piece = self.__chess.piece_at((x, y))
                if n_piece:
                    # if we hit an oppenents piece, take it
                    if (n_piece.color != piece.color) and take_pieces:
                        result.append((x, y))
                        return result
                    # else we have hit our own color and need to return
                    else:
                        return result
                # append the new move if no piece exists at the given coordinate
                else:
                    result.append((x, y))
            # return if we are out of range
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
        coords = self.__chess.piece_idx(piece)
        x = coords[0] + x_inc
        y = coords[1] + y_inc

        if Move.coord_in_range(x) and Move.coord_in_range(y):
            n_piece = self.__chess.piece_at((x, y))

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
    def coords_in_range(x: int,
                        y: int) -> bool:
        """
        Checks if the given coordinate is in bounds of the screen
        :param x: the given x value
        :param y: the given y value
        :return: boolean
        """
        return Move.coord_in_range(x) and Move.coord_in_range(y)
