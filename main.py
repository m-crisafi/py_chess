import pygame, utils
from models.chess import Chess
from config import configs
from render import Render
import models.move


def open_window():
    pygame.display.set_caption('Chess')

    return pygame.display.set_mode(
        ((configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"]) + configs["output_size"],
         (configs["padding"] * 2) + (configs["board_size"] * configs["cell_size"])),
        depth=32
    )


if __name__ == "__main__":
    running = True
    turn = "white"
    history = []
    images = utils.split_image("pieces.png")
    screen = open_window()
    pygame.init()
    chess = Chess()
    chess.load_board(images)
    stored_moves = models.move.get_all_moves(chess, "white")
    current_moves = models.move.get_all_moves(chess, "white")
    render = Render(screen, chess, history)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not chess.picked_up:
                    coords = pygame.mouse.get_pos()
                    point = render.screen_coords_to_point(coords)
                    if point and chess.has_piece_at(point[0], point[1]):
                        if chess.board[point[1]][point[0]].color == turn:
                            chess.pickup(point[0], point[1])
                            current_moves = models.move.moves_for_piece(chess, chess.picked_up)

            if event.type == pygame.MOUSEBUTTONUP:
                if chess.picked_up:
                    coords = pygame.mouse.get_pos()
                    point = render.screen_coords_to_point(coords)
                    if point and models.move.can_move(chess, chess.picked_up, point[0], point[1]):
                        move = chess.put_down(point[0], point[1])
                        history.append(move)
                        if turn == "white":
                            turn = "black"
                            current_moves = models.move.get_all_moves(chess, "black")
                        else:
                            turn = "white"
                            current_moves = models.move.get_all_moves(chess, "white")
                    else:
                        chess.return_piece()
                        current_moves = models.move.get_all_moves(chess, turn)

        if not chess.picked_up:
            coords = pygame.mouse.get_pos()
            point = render.screen_coords_to_point(coords)
            if point:
                hovered_piece = chess.board[point[1]][point[0]]
                if hovered_piece:
                    current_moves = models.move.moves_for_piece(chess, hovered_piece)
                else:
                    current_moves = stored_moves
            else:
                current_moves = stored_moves

        render.render(current_moves)
