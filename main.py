import pygame, utils
from models.chess import Chess
from config import configs
from render import Render
from models.move import Move


def open_window() -> pygame.Surface:
    """
    Opens the game window based on the settings in config.py
    :return: pygame.Surface
    """
    pygame.display.set_caption('Chess')

    return pygame.display.set_mode(
        ((configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"]) + configs["output_size"],
         (configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"])),
        depth=32
    )


def mouse_pos() -> (int, int):
    """
    Returns the current mosue position
    :return: (int, int)
    """
    return pygame.mouse.get_pos()


if __name__ == "__main__":
    # open our window and initialise pygame
    screen = open_window()
    pygame.init()

    # split up our pieces tilemap
    images = utils.split_image("pieces.png")
    
    running = True      # loop variable
    turn = "white"      # current turn
    history = []        # history of moves

    # initialise the main chess object
    chess = Chess()
    chess.load_board(images)

    # initialise the move checking object
    moves = Move(chess)
    moves.update()
    current_moves = moves.moves_for_color(turn)
    
    # initialise the rendering object
    render = Render(screen, chess, history)

    # run until we set the running variable to false
    while running:
        
        # get all events since the last loop
        for event in pygame.event.get():
            
            # on quit, set the loop condition variable to false
            if event.type == pygame.QUIT:
                running = False

            # on mouse button down check
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not chess.picked_up:
                    point = render.screen_coords_to_point(mouse_pos())
                    if point and chess.has_piece_at(point[0], point[1]):
                        if chess.board[point[1]][point[0]].color == turn:
                            chess.pickup(point[0], point[1])
                            current_moves = moves.moves_for_piece(chess.picked_up)

            # on mouse button up check
            if event.type == pygame.MOUSEBUTTONUP:
                if chess.picked_up:
                    point = render.screen_coords_to_point(mouse_pos())
                    if point and moves.can_move(chess.picked_up, (point[0], point[1])):
                        move = chess.put_down(point[0], point[1])
                        history.append(move)
                        if turn == "white":
                            turn = "black"
                        else:
                            turn = "white"
                        moves.update()
                        current_moves = moves.moves_for_color(turn)
                    else:
                        chess.return_piece()
                        current_moves = moves.moves_for_color(turn)

        # on hover check
        if not chess.picked_up:
            point = render.screen_coords_to_point(mouse_pos())
            if point:
                hovered_piece = chess.board[point[1]][point[0]]
                if hovered_piece and hovered_piece.color == turn:
                    current_moves = moves.moves_for_piece(hovered_piece)
                else:
                    current_moves = moves.moves_for_color(turn)
            else:
                current_moves = moves.moves_for_color(turn)

        render.render(current_moves)
