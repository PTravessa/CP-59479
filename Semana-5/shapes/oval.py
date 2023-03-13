from shape import Shape


class Oval(Shape):
    """
    Oval is a subclass of Shape that defines a oval or ellipse with
    axis parallel to the horizontal and vertical axis.
    """
    def __init__(self, fillPattern, border, center, rx, ry):
        """
        __init__ the Oval constructor

        Args:
            fillPattern (FillPattern): the color used to fill the shape
            border (LinePattern): color and thickness of the border
            center (Point2D): the position of the center
            rx (integer): the size of the horizontal radius
            ry (integer): the size of the vertical radius
        """
        super().__init__(fillPattern, border)
        self.center = center
        self.rx = rx
        self.ry = ry
