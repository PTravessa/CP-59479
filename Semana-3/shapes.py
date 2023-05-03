class Shape:
    def __init__(self, type, color, border, width, height):
        """Initializing a Class method for the shapes represented in PDF given in Moodle
        Seeking to reach the common characteristics and make a functional class for every object
        Args:
            type (Format Type): Format of the shape in question
            color (Self explanatory): The color present in each shape
            border (Type of border line fillment)
            width \height (Represents the limit characteristic of the object)
        """        
        self.type = type
        self.color = color
        self.border = border
        self.width = width
        self.height = height