from shape import Shape


class Rectangle(Shape):
    """
    Rectangle a sub-class of Shape that defines a rectangle.
    """
    def __init__(self, fillPattern, border, ul, lr):
        """
        __init__ Rectangle constructor

        Args:
            fillPattern (FillPattern): the color used to fill the shape
            border (LinePattern): color and thickness of the border
            ul (Point2D): upper-left corner of the rectangle
            lr (Point2D): lower-right corner of the rectangle
        """
        super().__init__(fillPattern, border)
        self.ul = ul
        self.lr = lr
