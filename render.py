import pygame
import utils
from configs import configs
from models.chess import Chess
from models.selector import Selector

WHITE = (255, 255, 255)
BACKGROUND = (198, 167, 133)
BLACK = (0, 0, 0)
HIGHLIGHT_YELLOW = (200, 200, 29, 255)
LAST_MOVE_HIGHLIGHT = (150, 150, 29, 255)
ALPHA = 128


class Render:

    def __init__(self,
                 screen: pygame.surface,
                 chess: Chess):
        """
        Constructs our renderer by pre calculating all the screen sizes
        :param screen: the given pygame window
        :param chess: the given game object (pointer)
        """
        self.s = configs["board_size"]               # board size in cells
        self.cs = configs["cell_size"]               # cell size
        self.p = configs["padding"]                  # border padding
        self.dw = configs["output_size"]             # output display width
        self.op = configs["output_padding"]          # display text padding
        self.bs = self.s * self.cs                   # board abs size
        self.ds = self.bs + (self.p * 2)             # abs display xy start
        self.sw = self.bs + (self.p * 2) + self.dw   # screen abs width
        self.sh = self.bs + (self.p * 2) + self.dw   # screen abs height
        # pointers to game objects
        self.screen = screen
        self.chess = chess
        # load the board png
        self.board_png = utils.load_and_scale("board.png")
        # load the font for drawing the border
        self.border_font = pygame.font.SysFont("arial", int(self.p / 3), bold=True)
        self.display_font = pygame.font.SysFont("arial", configs["output_text_size"], bold=True)

    def render(self,
               current_moves: (str, [(int, int)]) = None,
               selector: Selector = None) -> None:
        """
        Main render function
        :param current_moves: the list of available moves as coordinates
        :param selector: the currently selector
        :return: None
        """
        self.screen.fill(BACKGROUND)
        self.__draw_board()
        self.__draw_border()

        if current_moves:
            self.__draw_current_moves(current_moves)

        self.__draw_display()
        self.__draw_pieces()

        if selector:
            self.__draw_selection_overlay(selector)

        pygame.display.update()

    def __draw_board(self) -> None:
        """
        Draws the board to the screen
        :return: None
        """
        rect = pygame.Rect(
            (self.p, self.p),
            (self.s, self.s))
        self.screen.blit(self.board_png, rect)

    def __draw_border(self) -> None:
        """
        Renders the letters and numbers to the boards border
        :return: None
        """
        # iterate across the screen and draw the letters
        for x in range(self.s):
            label = self.border_font.render(utils.idx_to_letter(x), True, BLACK)
            # get our labels (x, y) position and write it the screen
            x_start = self.p + (x * self.cs)
            y_top = (self.p / 2) - (label.get_height() / 2)
            y_bottom = self.p + self.bs + y_top
            coords = (x_start + (self.cs / 2) - (label.get_width() / 2),
                      y_top)
            self.screen.blit(label, coords)
            coords = (x_start + (self.cs / 2) - (label.get_width() / 2),
                      y_bottom)
            self.screen.blit(label, coords)

        # iterate down the screen and draw the numbers
        for y in range(self.s):
            # invert the index draw 8...1
            new_y = (y - self.s + 1) * -1
            label = self.border_font.render(str(new_y + 1), True, BLACK)

            y_start = self.p + (new_y * self.cs)
            x_left = (self.p / 2) - (label.get_width() / 2)
            x_right = self.p + self.bs + x_left
            coords = (x_left,
                      y_start + (self.cs / 2) - (label.get_height() / 2))
            self.screen.blit(label, coords)
            coords = (x_right,
                      y_start + (self.cs / 2) - (label.get_height() / 2))
            self.screen.blit(label, coords)

    def __draw_display(self) -> None:
        """
        Draws all previous moves to the output display
        :return: None
        """
        for idx, move in enumerate(self.chess.history):
            piece = self.chess.piece_for_id(move.piece_id)
            move_string = "%s %s %s" % (piece.key.title(),
                                        utils.coord_to_notation(move.start_coords),
                                        utils.coord_to_notation(move.end_coords))
            if piece.color == "white":
                label = self.display_font.render(move_string, True, WHITE)
            else:
                label = self.display_font.render(move_string, True, BLACK)

            coords = (self.ds + self.op,
                      self.p + (idx * (label.get_height() + 5)))
            self.screen.blit(label, coords)

    def __draw_pieces(self) -> None:
        """
        Renders every piece to the screen
        :return: None
        """
        # iterate all the pieces and render them
        for y in range(self.s):
            for x in range(self.s):
                piece = self.chess.board[y][x]

                if piece:
                    rect = pygame.Rect(
                        (self.p + (self.cs * x),
                         self.p + (self.cs * y)),
                        (self.cs,
                         self.cs))
                    self.screen.blit(piece.img, rect)

        # render the picked up piece
        if self.chess.picked_up:
            coords = pygame.mouse.get_pos()
            rect = pygame.Rect(
                (coords[0] - (self.cs / 2),
                 coords[1] - (self.cs / 2)),
                (self.cs,
                 self.cs))
            self.screen.blit(self.chess.picked_up.img, rect)

    def __draw_current_moves(self,
                             current_moves: (str, [(int, int)])) -> None:
        """
        Generates an alpha layer and highlights any cells that can be moved to by the player
        :param current_moves: list of valid move coordinates
        :return: None
        """
        # generate the alpha layer
        s = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        s.fill((255, 255, 255, 0))

        # draw the last move
        if configs["show_last_move"]:
            last_move = self.chess.last_move()
            if last_move:
                start = pygame.Rect(
                    (self.p + (self.cs * last_move.start_coords[0]),
                     self.p + (self.cs * last_move.start_coords[1])),
                    (self.cs,
                     self.cs))

                end = pygame.Rect(
                    (self.p + (self.cs * last_move.end_coords[0]),
                     self.p + (self.cs * last_move.end_coords[1])),
                    (self.cs,
                     self.cs))

                pygame.draw.rect(s, LAST_MOVE_HIGHLIGHT, start)
                pygame.draw.rect(s, LAST_MOVE_HIGHLIGHT, end)

        if (configs["show_piece_moves"] and current_moves[0] == "piece") or \
           (configs["show_team_moves"] and current_moves[0] == "team"):

            for coord in current_moves[1]:
                rect = pygame.Rect(
                    (self.p + (self.cs * coord[0]),
                     self.p + (self.cs * coord[1])),
                    (self.cs,
                     self.cs))
                pygame.draw.rect(s, HIGHLIGHT_YELLOW, rect)

        # write it to our main screen
        self.screen.blit(s, (0, 0))

    def __draw_selection_overlay(self,
                                 selector: Selector) -> None:
        """
        Draws the selection overlay to the screen
        :param selector: the given selector
        :return: None
        """
        img_size = self.chess.pieces[0].img.get_height()

        width = img_size * len(selector.pieces)
        height = img_size
        x_start = self.p + (self.bs / 2) - (width / 2)
        y_start = self.p + (self.bs / 2) - (height / 2)

        rect = pygame.Rect(x_start, y_start, width, height)

        pygame.draw.rect(self.screen, WHITE, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)

        for idx, piece in enumerate(selector.pieces):
            rect = pygame.Rect(
                x_start + (idx * img_size),
                y_start,
                img_size,
                img_size)

            if idx == selector.selected_index:
                pygame.draw.rect(self.screen, HIGHLIGHT_YELLOW, rect)

            pygame.draw.rect(self.screen, BLACK, rect, 1)
            self.screen.blit(piece.img, rect)

    def in_board_bounds(self,
                        point: (int, int)) -> bool:
        """
        Returns if the given abs coordinates are in bounds of the boards abs position
        :param point: the given abs coordinates
        :return: bool
        """
        return (self.p < point[0] < (self.p + self.bs)) and \
               (self.p < point[1] < (self.p + self.bs))

    def screen_coords_to_point(self,
                               point: (int, int)) -> (int, int):
        """
        Returns the board indices for the given abs coordinate
        :param point: the given abs coordinates
        :return: (int, int)
        """
        if self.in_board_bounds(point):
            return (
                int((point[0] - self.p) / self.cs),
                int((point[1] - self.p) / self.cs)
            )
        return None
