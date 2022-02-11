import pygame, utils
from config import configs

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (250, 237, 29)
ALPHA = 192


class Render:

    def __init__(self, screen, chess):
        self.w = configs["width"]
        self.h = configs["height"]
        self.cs = configs["cell_size"]
        self.p = configs["padding"]
        self.bw = self.w * self.cs
        self.bh = self.h * self.cs
        self.sw = self.bw + (self.p * 2)
        self.sh = self.bh + (self.p * 2)
        self.board_png = utils.load_and_scale("board.png")
        self.screen = screen
        self.chess = chess
        self.font = pygame.font.SysFont("arial", int(self.p / 3))

    def render(self, current_moves):
        self.screen.fill(WHITE)
        self.__draw_board()
        self.__draw_border()
        self.__draw_curent_moves(current_moves)
        self.__draw_pieces()
        pygame.display.update()

    def __draw_board(self):
        rect = pygame.Rect(
            (self.p, self.p),
            (self.w, self.h))
        self.screen.blit(self.board_png, rect)

    def __draw_border(self):
        for x in range(self.w):
            label = self.font.render(utils.idx_to_letter(x), True, BLACK)

            x_start = self.p + (x * self.cs)
            y_start = (self.p / 2) - (label.get_height() / 2)
            coords = (x_start + (self.cs / 2) - (label.get_width() / 2),
                      y_start)
            self.screen.blit(label, coords)

        for y in range(self.h):
            new_y = (y - self.h + 1) * -1
            label = self.font.render(str(new_y + 1), True, BLACK)

            x_start = (self.p / 2) - (label.get_width() / 2)
            y_start = self.p + (new_y * self.cs)
            coords = (x_start,
                      y_start + (self.cs / 2) - (label.get_height() / 2))
            self.screen.blit(label, coords)

    def __draw_pieces(self):
        for y in range(self.h):
            for x in range(self.w):
                piece = self.chess.board[y][x]

                if piece:
                    rect = pygame.Rect(
                        (self.p + (self.cs * x),
                         self.p + (self.cs * y)),
                        (self.cs,
                         self.cs))
                    self.screen.blit(piece.img, rect)

        if self.chess.picked_up:
            coords = pygame.mouse.get_pos()
            rect = pygame.Rect(
                (coords[0] - (self.cs / 2),
                 coords[1] - (self.cs / 2)),
                (self.cs,
                 self.cs))
            self.screen.blit(self.chess.picked_up.img, rect)

    def __draw_curent_moves(self, current_moves):
        s = pygame.Surface((self.sw, self.sh))
        s.set_alpha(ALPHA)

        for coord in current_moves:
            rect = pygame.Rect(
                (self.p + (self.cs * coord[0]),
                 self.p + (self.cs * coord[1])),
                (self.cs,
                 self.cs))
            pygame.draw.rect(s, HIGHLIGHT, rect)

        self.screen.blit(s, (0, 0))

    def in_board_bounds(self, point):
        return (self.p < point[0] < (self.sw - self.p)) and \
               (self.p < point[1] < (self.sw - self.p))

    def screen_coords_to_point(self, point):
        if self.in_board_bounds(point):
            return (
                int((point[0] - self.p) / self.cs),
                int((point[1] - self.p) / self.cs)
            )
        return None





