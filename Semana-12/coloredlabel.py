import kivy

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class ColoredLabel(Label):
    """
    ColoredLabel is a subclass of Label that permits the definition of a
    background color easily.
    """
    def __init__(self, background_color=(0, 0, 0, 1),
                 color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.italic = True
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle()
            self.rect.pos = self.pos
            self.rect.size = self.size
        self.bind(pos=self.__update_rect, size=self.__update_rect)

    @staticmethod
    def __update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

# Local Variables:
# coding: utf-8
# End:
