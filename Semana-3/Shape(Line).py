from shapes import Shape

class Line(Shape):
    def __init__(self, type, color, border, width, height,
                 angle, arrow):
        """Shape sub class for Lines

        Args:
            type (Format Type): Line
            color (Self explanatory): Black
            border (Type of border line fillment): Not present
            width \height (Represents the limit characteristic of the object)
            angle (_type_): Direction angle
            arrows (_type_): Present or Not Present
        """        
        super().__init__(type, color, border, width, height, angle, arrow)
        self.angle = angle
        self.arrow = arrow