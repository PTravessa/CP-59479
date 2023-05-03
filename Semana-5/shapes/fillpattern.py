class FillPattern:
    """
     FillPattern represents how a shape can be filled. 
     In this version the pattern corresponds to a color.
    """
    def ___init__(self, color):
        """
        ___init__ The FillPattern constructor

        Args:
            color (Color): the color used to fill the area.
        """
        self.color = color
