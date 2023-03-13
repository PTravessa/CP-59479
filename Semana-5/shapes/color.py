class Color:
    """
     The color class represents a color as its red, green, 
     blue and alpha channel (opacity) components.
    """
    def __init__(self, r, g, b, a):
        """
        __init__ Construtor for Color

        Args:
            r (integer): red component [0..1]
            g (integer): green component [0..1]
            b (integer): blue component [0..1] 
            a (integer): alpha component [0..1]
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
