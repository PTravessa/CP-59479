from line import Line


class Arrow(Line):
    """
    Arrow extends Line and represents an arrow the position 
    of the head can be specified via the arrowPos attribute.
    """
    def __init__(self, linePattern, start, end, arrowPos):
        """
        __init__ Arrow constructor

        Args:
            linePattern (LinePattern): Defines the color  
            start (Point2D): starting point
            end (Point2D): ending point
            arrowPos (string): the value must be 'start' or 'end'
        """
        super().__init__(linePattern, start, end)
        self.arrowPos = arrowPos
