
class Move:

    def __init__(self,
                 piece_id: int,
                 from_coord: (int, int),
                 to_coord: (int, int),
                 took_piece: bool):
        """
        Constructs a move from the given parameters
        :param piece_id: the id of the piece
        :param from_coord: the coordinate the move came from
        :param to_coord: the coordinate the move ended in
        :param took_piece: if a piece was taken
        """
        self.piece_id = piece_id
        self.from_coord = from_coord
        self.to_coord = to_coord
        self.took_piece = took_piece
