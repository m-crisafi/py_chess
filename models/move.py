from config import configs
from models.chess import Chess
from models.piece import Piece


def moves_for_piece(chess: Chess,
                    piece: Piece) -> [(int, int)]:
    """
    Checks all possible moves for a given piece
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    # check the type of each piece and call the appropriate function
    if piece.key == "bishop":
        result.extend(bishop(chess, piece))
    elif piece.key == "rook":
        result.extend(rook(chess, piece))
    elif piece.key == "knight":
        result.extend(knight(chess, piece))
    elif piece.key == "queen":
        result.extend(queen(chess, piece))
    elif piece.key == "king":
        result.extend(king(chess, piece))
    elif piece.key == "pawn":
        result.extend(pawn(chess, piece))

    return result


def can_move(chess: Chess,
             piece: Piece,
             x: int,
             y: int) -> bool:
    """
    Checks a given piece can move to a given coordinate
    :param chess: the curent game state
    :param piece: the given piece
    :param x: the given x position
    :param y: the given y position
    :return: bool
    """
    # check our piece is not in its starting position
    if chess.last_position == (x, y):
        return False
    # get all possible moves the piece can make
    result = moves_for_piece(chess, piece)
    # check if it can move to the given coordinate
    for coord in result:
        if (x, y) == coord:
            return True
    return False


def get_all_moves(chess: Chess,
                  color: str) -> [(int, int)]:
    """
    Returns all avaliable moves for the current player
    :param chess: the current game state
    :param color: the given player color
    :return: [(x, y)]
    """
    result = []
    for piece in chess.pieces:
        if piece.color == color:
            result.extend(moves_for_piece(chess, piece))
    return result


def bishop(chess: Chess,
           piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given bishop
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    return trace_diagonals(chess, piece)


def rook(chess: Chess,
         piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given rook
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    return trace_vertical_horizontal(chess, piece)


def knight(chess: Chess,
           piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given knight
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    coords = chess.piece_idx(piece)
    # up left / up right / down left / down right / left up / left down / right up / right down
    result.extend(check_relative_to_piece(chess, piece, -1, -2))
    result.extend(check_relative_to_piece(chess, piece, 1, -2))
    result.extend(check_relative_to_piece(chess, piece, -1, 2))
    result.extend(check_relative_to_piece(chess, piece, 1, 2))
    result.extend(check_relative_to_piece(chess, piece, -2, -1))
    result.extend(check_relative_to_piece(chess, piece, -2, 1))
    result.extend(check_relative_to_piece(chess, piece, 2, 1))
    result.extend(check_relative_to_piece(chess, piece, 2, -1))
    return result


def queen(chess: Chess,
          piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given queen
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    result.extend(trace_diagonals(chess, piece))
    result.extend(trace_vertical_horizontal(chess, piece))
    return result


def king(chess: Chess,
         piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given king
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    result.extend(trace_diagonals(chess, piece, count=1))
    result.extend(trace_vertical_horizontal(chess, piece, count=1))
    result.extend(check_castling(chess, piece))
    return result


def pawn(chess: Chess,
         piece: Piece) -> [(int, int)]:
    """
    Returns all moves for the given black pawn
    :param chess: the current game state
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

    result.extend(trace(chess, piece, 0, y_inc, count=count, take_pieces=False))

    # check left an right diagonals
    for i in range(-1, 2, 2):
        c = chess.piece_idx(piece)
        x = c[0] + i
        y = c[1] + y_inc

        if coord_in_range(x) and coord_in_range(y):
            n_piece = chess.board[y][x]
            if n_piece and (n_piece.color != piece.color):
                result.append((x, y))

    return result


def check_castling(chess: Chess,
                   king: Piece) -> [(int, int)]:
    result = []

    if king.key == "king" and not king.has_moved:
        coords = chess.piece_idx(king)
        for step in range(-1, 2, 2):
            for x in range(1, configs["board_size"]):
                if coord_in_range(x):
                    n_piece = chess.board[coords[1]][coords[0] + (step * x)]
                    if not n_piece:
                        continue
                    if n_piece.color == king.color and \
                       n_piece.key == "rook" and \
                       not n_piece.has_moved:
                        if step < 0:
                            result.append((coords[0] - 2, coords[1]))
                            break
                        else:
                            result.append((coords[0] + 2, coords[1]))
                            break
                    else:
                        break
    else:
        return result

    return result


def trace_diagonals(chess: Chess,
                    piece: Piece,
                    count: int = configs["board_size"]) -> [(int, int)]:
    """
    Traces all diagonals from the given piece
    :param chess: the current game state
    :param piece: the given piece
    :param count: how far to count from the given piece
    :return:
    """
    result = []
    # top left / top right / bottom left / bottom right
    result.extend(trace(chess, piece, -1, -1, count))
    result.extend(trace(chess, piece, 1, -1, count))
    result.extend(trace(chess, piece, -1, 1, count))
    result.extend(trace(chess, piece, 1, 1, count))
    return result


def trace_vertical_horizontal(chess: Chess,
                              piece: Piece,
                              count: int = configs["board_size"]) -> [(int, int)]:
    """
    Traces all vertical and horizontal lines from the given piece
    :param chess: the current game state
    :param piece: the given piece
    :param count: how far to count from the given piece
    :return:
    """
    result = []
    # up / down / left / right
    result.extend(trace(chess, piece, 0, -1, count))
    result.extend(trace(chess, piece, 0, 1, count))
    result.extend(trace(chess, piece, -1, 0, count))
    result.extend(trace(chess, piece, 1, 0, count))
    return result


def trace(chess: Chess,
          piece: Piece,
          x_inc: int,
          y_inc: int,
          count: int,
          take_pieces: bool = True) -> [(int, int)]:
    """
    Traces along the x, y plane from the given piece until it hits the count or another piece
    :param chess: the current game state
    :param piece: the given piece
    :param x_inc: the increment direction on the x plane
    :param y_inc: the increment direction on the y plane
    :param count: how far to count from the given piece
    :param take_pieces: take any opposing colours pieces
    :return: [(x, y)]
    """
    result = []
    coords = chess.piece_idx(piece)
    x = coords[0]
    y = coords[1]
    step = 0

    while step != count:
        x += x_inc
        y += y_inc
        if coord_in_range(x) and coord_in_range(y):
            n_piece = chess.board[y][x]
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


def check_relative_to_piece(chess: Chess,
                            piece: Piece,
                            x_inc: int,
                            y_inc: int) -> (int, int):
    """
    Checks if piece can move to the coordinate x_inc and y_inc from the give npiece
    :param chess:
    :param piece:
    :param x_inc:
    :param y_inc:
    :return:
    """
    result = []
    coords = chess.piece_idx(piece)
    x = coords[0] + x_inc
    y = coords[1] + y_inc

    if coord_in_range(x) and coord_in_range(y):
        n_piece = chess.board[y][x]

        if not n_piece or (n_piece and n_piece.color != piece.color):
            result.append((x, y))
            return result

    return result


def coord_in_range(coord: int) -> bool:
    """
    Checks if the given coordinate value is in bounds of the screen
    :param coord:
    :return: boolean
    """
    return 0 <= coord < configs["board_size"]


def coords_int_range(x, y) -> bool:
    """
    Checks if the given coordinate is in bounds of the screen
    :param x: the given x value
    :param y: the given y value
    :return: boolean
    """
    return coord_in_range(x) and coord_in_range(y)
