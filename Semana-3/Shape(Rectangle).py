from shapes import Shape

class Rectangle(Shape):
    def __init__(self, type, color, border, width, height,
                 hasText):
        """Shape sub class for Rectangle/Square

        Args:
            type (Format Type): Rectangle/Square
            color (Self explanatory): Blue or None
            border (Type of border line fillment): Red or Not present
            width \height (Represents the limit characteristic of the object)
            hasText (boolean?): Is there written text or Not
        """        
        super().__init__(type, color, border, width, height, hasText)
        self.hasText = hasText