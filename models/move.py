
class Move:

    def __init__(self,
                 piece_id: int,
                 start_coords: (int, int),
                 end_coords: (int, int),
                 took_piece: int = -1):
        """
        Contstructor for the move object
        :param piece_id: the given piece id
        :param start_coords: the start coordinates for the move
        :param end_coords: the end coordinates for the move
        :param took_piece: the id of the taken piece, -1 if not piece taken
        """
        self.piece_id = piece_id
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.took_piece = took_piece
