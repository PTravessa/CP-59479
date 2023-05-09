
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class ColoredBoxLayout(BoxLayout):
    def __init__(self, background_color=(231/255, 98/255, 203/255, 1),
                 **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle()
            self.rect.pos = self.pos
            self.rect.size = self.size
        self.bind(pos=ColoredBoxLayout.__update_rect,
                  size=ColoredBoxLayout.__update_rect)

    @staticmethod
    def __update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
