class Line:
    """
    Line represents a line drawn between two points
    """
    def __init__(self, linePattern, start, end):
        """
        __init__ Line constructor

        Args:
            linePattern (LinePattern): Defines the color  
            start (Point2D): starting point
            end (Point2D): ending point
        """
        self.linePattern = linePattern
        self.start = start
        self.end = end
