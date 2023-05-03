
class Point2D:
    """
     Point2D represents a point in 2D. The coordinates correspond
     to the position of screen pixels are integers. The origin is
     the upper left corner.
    """
    def __init__(self, x, y):
        """
        __init__ Constutor for Point2D

        Args:
            x (integer): horizontal axis coordinate
            y (integer): vertical axis coordinate
        """
        self.x = x
        self.y = y
