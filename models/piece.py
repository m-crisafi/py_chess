
class Piece:

    def __init__(self, id, key, img, color, has_moved):
        """
        :param id: unique piece identifier
        :param key: the pieces type
        :param img: bitmap image
        :param color: the pieces color (white / black)
        :param has_moved: set to true on first move
        """
        self.id = id
        self.key = key
        self.img = img
        self.color = color
        self.has_moved = has_moved

    def compare_color(self,
                      color: str) -> bool:
        """
        Returns true if the given color matches piece.color
        :param color: the given color
        :return: bool
        """
        return self.color == color
