class Text:
    """
     Text represents a text graphical element. The text will
     be drawn horizontally starting at a given position
    """
    def __init__(self, fontname, size, color, position):
        """
        __init__ Text constructor

        Args:
            fontname (string): the name of the font
            size (integer): font size
            color (Color): text color
            position (Point): the position of the lower 
            left corner of the first letter.
        """
        self.fontname = fontname
        self.size = size
        self.color = color
        self.position = position
