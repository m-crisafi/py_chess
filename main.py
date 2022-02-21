import pygame
import utils
from configs import configs
from models.selector import Selector
from render import Render
from models.checker import Checker
from models.chess import Chess
from factory import Factory


def open_window() -> pygame.Surface:
    """
    Opens the game window based on the settings in configs.py
    :return: pygame.Surface
    """
    pygame.display.set_caption('Chess')

    return pygame.display.set_mode(
        # set mode takes an (int, int) tuple as the screen size
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

    # loop variable
    running = True
    factory = Factory(images)

    # initialise the main chess object
    chess = Chess()
    chess.load_board(factory)

    # initialise the move checking object
    checker = Checker(chess)
    checker.update()
    current_moves = checker.moves_for_team()

    # initialise the rendering object
    render = Render(screen, chess)

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
                    if point and chess.has_piece_at_coord(point):
                        # ensure the piece is of the correct color
                        if chess.piece_at(point).color == chess.turn:
                            # pick up the piece and load current moves
                            chess.pickup(point[0], point[1])
                            current_moves = checker.moves_for_piece(chess.picked_up)

                # on put down
                else:
                    point = render.screen_coords_to_point(mouse_pos())
                    # ensure we have clicked the screen and the piece can move there
                    if point and checker.can_move(chess.picked_up, (point[0], point[1])):
                        # put the piece down and update if successful
                        if chess.put_down(point[0], point[1]):
                            checker.update()
                            current_moves = checker.moves_for_team()
                    # return the piece if we have clicked an invalid location
                    else:
                        chess.return_piece()
                        current_moves = checker.moves_for_team()

            # check keyboard inputs
            if event.type == pygame.KEYUP:
                # toggle show piece moves
                if event.key == pygame.K_s:
                    configs["show_piece_moves"] = not configs["show_piece_moves"]
                # toggle show team moves
                if event.key == pygame.K_a:
                    configs["show_team_moves"] = not configs["show_team_moves"]
                if event.key == pygame.K_d:
                    configs["show_last_move"] = not configs["show_last_move"]
                if event.key == pygame.K_f:
                    fen = factory.to_fen_string(chess.board)

        # on hover check
        if not chess.picked_up:
            # get the mouse pos and check covert it to (x, y) if it is on the board
            point = render.screen_coords_to_point(mouse_pos())
            if point:
                # get the piece we are hovering over
                hovered_piece = chess.piece_at(point)
                # if it exists and its of the current players color, load the pieces moves
                if hovered_piece and hovered_piece.color == chess.turn:
                    current_moves = checker.moves_for_piece(hovered_piece)
                # load the teams moves if not
                else:
                    current_moves = checker.moves_for_team()
            else:
                current_moves = checker.moves_for_team()

        # check for pawn promotion
        if chess.pawn_promotion:
            selector = Selector(factory.generate_promotion_pieces(utils.invert_team_color(chess.turn)))
            selected = False

            while not selected:
                render.render(selector=selector)

                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        # toggle show piece moves
                        if event.key == pygame.K_LEFT:
                            selector.scroll_left()
                        # toggle show team moves
                        if event.key == pygame.K_RIGHT:
                            selector.scroll_right()
                        if event.key == pygame.K_SPACE:
                            selected = True

            chess.pawn_promotion = False
            move = chess.last_move()
            chess.replace_piece(selector.get_selected_piece(), move.end_coords)

        # render the board
        render.render(current_moves)
