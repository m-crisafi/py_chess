from config import configs
from models.chess import Chess
from models.piece import Piece


def moves_for_piece(chess: Chess, piece: Piece):
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
        if piece.color == "white":
            result.extend(w_pawn(chess, piece))
        else:
            result.extend(b_pawn(chess, piece))

    return result


def can_move(chess: Chess, piece: Piece, x: int, y: int):
    """
    Checks a given piece can move to a given coordinate
    :param chess: the curent game state
    :param piece: the given piece
    :param x: the given x position
    :param y: the given y position
    :return: boolean
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


def get_all_moves(chess: Chess, color: str):
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


def bishop(chess: Chess, piece: Piece):
    """
    Returns all moves for the given bishop
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    return trace_diagonals(chess, piece)


def rook(chess: Chess, piece: Piece):
    """
    Returns all moves for the given rook
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    return trace_vertical_hortizonal(chess, piece)


def knight(chess: Chess, piece: Piece):
    """
    Returns all moves for the given knight
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    return result


def queen(chess: Chess, piece: Piece):
    """
    Returns all moves for the given queen
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    result.extend(trace_diagonals(chess, piece))
    result.extend(trace_vertical_hortizonal(chess, piece))
    return result


def king(chess: Chess, piece: Piece):
    """
    Returns all moves for the given king
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    result.extend(trace_diagonals(chess, piece, count=1))
    result.extend(trace_vertical_hortizonal(chess, piece, count=1))
    return result


def b_pawn(chess: Chess, piece: Piece):
    """
    Returns all moves for the given black pawn
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    coords = chess.piece_idx(piece)
    if coords[1] == 1:
        result.extend(trace_vertical(chess, piece, 1, count=2))
    else:
        result.extend(trace_vertical(chess, piece, 1, count=1))
    return result


def w_pawn(chess: Chess, piece: Piece):
    """
    Returns all moves for the given white pawn
    :param chess: the current game state
    :param piece: the given piece
    :return: [(x, y)]
    """
    result = []
    coords = chess.piece_idx(piece)
    if coords[1] == configs["height"] - 2:
        result.extend(trace_vertical(chess, piece, -1, count=2))
    else:
        result.extend(trace_vertical(chess, piece, -1, count=1))
    return result


def trace_diagonals(chess: Chess, piece: Piece, count: int = configs["width"]):
    """

    :param chess:
    :param piece:
    :param count:
    :return:
    """
    result = []
    # top left / top right / bottom left / bottom right
    result.extend(trace_diagonal(chess, piece, -1, -1, count))
    result.extend(trace_diagonal(chess, piece, 1, -1, count))
    result.extend(trace_diagonal(chess, piece, -1, 1, count))
    result.extend(trace_diagonal(chess, piece, 1, 1, count))
    return result


def trace_vertical_hortizonal(chess: Chess, piece: Piece, count: int = configs["height"]):
    """

    :param chess:
    :param piece:
    :param count:
    :return:
    """
    result = []
    # up / down / left / right
    result.extend(trace_vertical(chess, piece, -1, count))
    result.extend(trace_vertical(chess, piece, 1, count))
    result.extend(trace_horizontal(chess, piece, -1, count))
    result.extend(trace_horizontal(chess, piece, 1, count))
    return result


def trace_vertical(chess: Chess,
                   piece: Piece,
                   inc: int,
                   count: int = configs["height"]):
    """

    :param chess:
    :param piece:
    :param inc:
    :param count:
    :return:
    """
    result = []
    coords = chess.piece_idx(piece)
    x = coords[0]
    y = coords[1]
    step = 0

    while step != count:
        y += inc
        if y_in_range(y):
            n_piece = chess.board[y][x]
            if n_piece:
                if n_piece.color != piece.color:
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


def trace_horizontal(chess: Chess,
                     piece: Piece,
                     inc: int,
                     count: int =
                     configs["width"]):
    """

    :param chess:
    :param piece:
    :param inc:
    :param count:
    :return:
    """
    result = []
    coords = chess.piece_idx(piece)
    x = coords[0]
    y = coords[1]
    step = 0

    while step != count:
        x += inc
        if x_in_range(x):
            n_piece = chess.board[y][x]
            if n_piece:
                if n_piece.color != piece.color:
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


def trace_diagonal(chess: Chess,
                   piece: Piece,
                   x_inc: int,
                   y_inc: int,
                   count: int):
    """

    :param chess:
    :param piece:
    :param x_inc:
    :param y_inc:
    :param count:
    :return:
    """
    result = []
    coords = chess.piece_idx(piece)
    x = coords[0]
    y = coords[1]
    step = 0

    while step != count:
        x += x_inc
        y += y_inc
        if x_in_range(x) and y_in_range(y):
            n_piece = chess.board[y][x]
            if n_piece:
                if n_piece.color != piece.color:
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


def x_in_range(x: int):
    """

    :param x:
    :return:
    """
    return 0 <= x < configs["width"]


def y_in_range(y: int):
    """

    :param y:
    :return:
    """
    return 0 <= y < configs["height"]
