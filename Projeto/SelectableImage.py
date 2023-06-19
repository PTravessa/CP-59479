
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
class SelectableImage(CheckBox, ButtonBehavior):
    selected_images = dict()

    def __init__(self, image_source, id, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''  # Remove default background
        self.group = 'images'
        self.image_source = image_source
        self.id = id

        self.image = Image(source=self.image_source)
        self.add_widget(self.image)

        with self.canvas.before:
            self.frame_color = Color(1, 1, 1, 1)  # White color
            self.frame = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_image_size, pos=self._update_image_pos)
        self.bind(active=self.on_active)

        if self.id in self.selected_images:
            self.frame_color.rgba = (1, 0, 0, 1)        

    def rotate(self):
        # im = Image.open(self.getImagefile())
        self.image.rotate(-90, expand=True)
        width, height = self.metadata['dimensions']
        self.image.metadata['dimensions'] = (height, width)
        self.image.reload()

    def on_active(self, instance, value):
        if value:
            self.frame_color.rgba = (1, 0, 0, 1)  # Red color when active
            if self.id not in self.selected_images:
                self.selected_images[self.id]=self  # Add self to selected_images list
            else:
                self.selected_images.pop(self.id)
                self.frame_color.rgba = (1, 1, 1, 1)
        else:
            if self.id not in self.selected_images:
                self.frame_color.rgba = (1, 1, 1, 1)
            else:
                self.frame_color.rgba = (1, 0, 0, 1)
            
        print(self.selected_images)

        """else: #removes the before selected image
            self.frame_color.rgba = (1, 1, 1, 1)  # White color when inactive
            if self in self.selected_images:
                self.selected_images.remove(self) """ # Remove self from selected_images list
        
        """else: #stores only one time the same file
            self.frame_color.rgba = (1, 1, 1, 1)  
            if self not in self.selected_images:
                self.selected_images.remove(self) """

        # Call the update_selected_images_label method from PicLib
        app = App.get_running_app()
        app.update_selected_images_label()
    
    def _update_image_size(self, *args):
        self.image.size = self.size
        self.frame.size = self.size

    def _update_image_pos(self, *args):
        self.image.pos = self.pos
        self.frame.pos = self.pos
