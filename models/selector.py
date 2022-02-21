from models.piece import Piece


class Selector:

    def __init__(self, pieces):
        """
        Constructor for the selector
        """
        self.pieces = pieces
        self.selected_index = 0

    def scroll_left(self) -> None:
        """
        Moves the selected index left if possible
        :return: None
        """
        if self.selected_index > 0:
            self.selected_index -= 1

    def scroll_right(self) -> None:
        """
        Moves the selected index right if possible
        :return: None
        """
        if self.selected_index < len(self.pieces) - 1:
            self.selected_index += 1

    def get_selected_piece(self) -> Piece:
        """
        Returns the currently selected piece
        :return: the selected Piece
        """
        return self.pieces[self.selected_index]
