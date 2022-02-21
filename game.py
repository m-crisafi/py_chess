import pygame
import utils
from configs import configs
from models.selector import Selector
from render import Render
from models.checker import Checker
from models.chess import Chess
from factory import Factory


STATE_RUNNING = "running"
STATE_PROMOTION = "promotion"


class Game:

    def __init__(self,
                 screen: pygame.Surface):
        """
        Initalised all the game variables
        :param screen:
        """
        self.images = None              # split up our pieces tile map
        self.running = True             # loop variable
        self.state = STATE_RUNNING      # game state variable
        self.factory = None             # factory object
        self.chess = Chess()            # chess object
        self.checker = None             # checker object
        self.current_moves = []
        self.screen = screen            # pointer to the screen object
        self.selector = None            # selector variable

        # initialise all the objects
        self.render = Render(self.screen, self.chess)
        self.images = utils.split_image("pieces.png")
        self.factory = Factory(self.images)
        self.chess.load_board(self.factory)
        self.checker = Checker(self.chess)
        self.checker.update()
        self.current_moves = self.checker.moves_for_team()

    @staticmethod
    def mouse_pos() -> (int, int):
        """
        Returns the current mouse position
        :return: (int, int)
        """
        return pygame.mouse.get_pos()

    def on_pickup(self) -> None:
        """
        Tries to pickup at the current mouse positon
        :return: None
        """
        # get the current mouse pos
        point = self.render.screen_coords_to_point(Game.mouse_pos())
        # ensure we have clicked the screen and we have a piece at that point
        if point and self.chess.has_piece_at_coord(point):
            # ensure the piece is of the correct color
            if self.chess.piece_at(point).color == self.chess.turn:
                # pick up the piece and load current moves
                self.chess.pickup(point[0], point[1])
                self.current_moves = self.checker.moves_for_piece(self.chess.picked_up)

    def on_putdown(self) -> None:
        """
        Tries to putdown at the given mouse position
        :return: None
        """
        # get the current mouse position
        point = self.render.screen_coords_to_point(Game.mouse_pos())
        # ensure we have clicked the screen and the piece can move there
        if point and self.checker.can_move(self.chess.picked_up, (point[0], point[1])):
            # put the piece down and update if successful
            if self.chess.put_down(point[0], point[1]):
                self.checker.update()
                self.current_moves = self.checker.moves_for_team()
        # return the piece if we have clicked an invalid location
        else:
            self.chess.return_piece()
            self.current_moves = self.checker.moves_for_team()

    def check_on_hover(self) -> None:
        """
        Checks the current mouse position and selects the appropriate move render type
        :return: None
        """
        # get the mouse pos and check covert it to (x, y) if it is on the board
        point = self.render.screen_coords_to_point(Game.mouse_pos())
        if point:
            # get the piece we are hovering over
            hovered_piece = self.chess.piece_at(point)
            # if it exists and its of the current players color, load the pieces moves
            if hovered_piece and hovered_piece.color == self.chess.turn:
                self.current_moves = self.checker.moves_for_piece(hovered_piece)
            # load the teams moves if not
            else:
                self.current_moves = self.checker.moves_for_team()
        else:
            self.current_moves = self.checker.moves_for_team()

    def handle_state_running_input(self) -> None:
        """
        Handles input for the running state
        :return: None
        """
        for event in pygame.event.get():

            # on quit, set the loop condition variable to false
            if event.type == pygame.QUIT:
                self.running = False

            # check mouse down input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.chess.picked_up:
                    self.on_pickup()
                else:
                    self.on_putdown()

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
                    print(self.factory.to_fen_string(self.chess.board))

    def handle_state_promotion_input(self) -> None:
        """
        Handles input for the promotion state
        :return: None
        """
        for event in pygame.event.get():
            # on quit, set the loop condition variable to false
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                # toggle show piece moves
                if event.key == pygame.K_LEFT:
                    self.selector.scroll_left()
                # toggle show team moves
                if event.key == pygame.K_RIGHT:
                    self.selector.scroll_right()
                if event.key == pygame.K_SPACE:
                    self.chess.pawn_promotion = False
                    move = self.chess.last_move()
                    self.chess.replace_with_new_piece(
                        self.selector.get_selected_piece(),
                        move.end_coords)
                    self.checker.update()
                    self.state = STATE_RUNNING

    def run(self):
        while self.running:
            if self.state == STATE_RUNNING:
                # check the pawn promotion condition
                if self.chess.pawn_promotion:
                    self.selector = Selector(
                        self.factory.generate_promotion_pieces(utils.invert_team_color(self.chess.turn)))
                    self.state = STATE_PROMOTION
                    continue

                # handle input
                self.handle_state_running_input()

                # check hover if we havent picked up a piece
                if not self.chess.picked_up:
                    self.check_on_hover()

                # render the screen
                self.render.render(current_moves=self.current_moves)
            else:
                self.handle_state_promotion_input()
                self.render.render(selector=self.selector)





