from PicLib_Phase1 import * #Must change the path for os.listdir
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage ,Image
from kivy.graphics import Rectangle, Color
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from zipfile import ZipFile
from PIL import Image as PILImage
import random
import math
import copy
class BrownBoxLayout(BoxLayout):
    # Class for brown box in label
    def __init__(self, background_color=(139/255, 69/255, 19/255, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle()
            self.rect.pos = self.pos
            self.rect.size = self.size
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size