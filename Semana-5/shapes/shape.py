class Shape:
    """
    Shape defines a generic shape, super-classe of all shapes
    This class must not be instanciated.
    """
    def __init__(self, fillPattern, border):
        """
        __init__ Shape constructor

        Args:
            fillPattern (FillPattern): the color used to fill the shape
            border (LinePattern): the color and thickness of the border.
        """
        self.fillPattern = fillPattern
        self.border = border
