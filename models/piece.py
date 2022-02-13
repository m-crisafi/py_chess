
class Piece:

    def __init__(self, key, img, color, has_moved):
        """
        :param key: the pieces type
        :param img: bitmap image
        :param color: the pieces color (white / black)
        :param has_moved: set to true on first move
        """
        self.key = key
        self.img = img
        self.color = color
        self.has_moved = has_moved
