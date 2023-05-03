class LinePattern:
    """
     LinePattern represents a pattern for a line. It is composed 
     by a line thickness and a color.
    """
    def __init_(self, thickness, color):
        """
        __init_ LinePattern constructor

        Args:
            thickness (double): a positive double value
            color (Color): the line color
        """
        self.thickness = thickness
        self.color = color

