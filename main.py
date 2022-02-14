import pygame, utils
from models.chess import Chess
from configs import configs
from render import Render
from models.move import Move


def open_window() -> pygame.Surface:
    """
    Opens the game window based on the settings in configs.py
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
    Returns the current mouse position
    :return: (int, int)
    """
    return pygame.mouse.get_pos()


if __name__ == "__main__":
    # open our window and initialise pygame
    screen = open_window()
    pygame.init()

    # split up our pieces tile map
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

            # check mouse down input
            if event.type == pygame.MOUSEBUTTONDOWN:

                # on pick up
                if not chess.picked_up:
                    point = render.screen_coords_to_point(mouse_pos())
                    # ensure we have clicked the screen and we have a piece at that point
                    if point and chess.has_piece_at(point[0], point[1]):
                        # ensure the piece is of the correct color
                        if chess.board[point[1]][point[0]].color == turn:
                            # pick up the piece and load current moves
                            chess.pickup(point[0], point[1])
                            current_moves = moves.moves_for_piece(chess.picked_up)

                # on put down
                else:
                    point = render.screen_coords_to_point(mouse_pos())
                    # ensure we have clicked the screen and the piece can move there
                    if point and moves.can_move(chess.picked_up, (point[0], point[1])):
                        # put the piece down and record it
                        move = chess.put_down(point[0], point[1])
                        history.append(move)
                        # move to the next turn by updating the move object and loading the current moves
                        turn = utils.invert_team_color(turn)
                        moves.update()
                        current_moves = moves.moves_for_color(turn)
                    # return the piece if we have clicked an invalid location
                    else:
                        chess.return_piece()
                        current_moves = moves.moves_for_color(turn)

            # check keyboard inputs
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    configs["show_piece_moves"] = not configs["show_piece_moves"]
                if event.key == pygame.K_a:
                    configs["show_team_moves"] = not configs["show_team_moves"]

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

        # render the board
        render.render(current_moves)
