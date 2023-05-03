from shapes import Shape
class Circle(Shape):
    def __init__(self, type, color, border, width, height):
        """Shape sub class for Circle

        Args:
            type (Format Type): Circle
            color (Self explanatory): Orange; Blue
            border (Type of border line fillment): Line Border with Purple color
            width \height (Represents the limit characteristic of the object)
        """        
        super().__init__(type, color, border, width, height)