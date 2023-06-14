import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.graphics import Rectangle, Color

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


class PicLib(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_row = None  # BoxLayout
        self.bottom_row = None  # BoxLayout
        self.main_panel = None  # BoxLayout

    def build(self):
        self.create_top_row()
        self.create_bottom_row()
        self.create_main_panel()

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.top_row)
        main_layout.add_widget(self.main_panel)
        main_layout.add_widget(self.bottom_row)

        return main_layout

    def create_top_row(self):
        self.top_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_row_label = Label(text='PicLib', font_size=40)
        self.top_row.add_widget(top_row_label)

    def create_bottom_row(self):
        self.bottom_row = BrownBoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        bottom_row_label = Label(text='Main Page', font_size=30)
        self.bottom_row.add_widget(bottom_row_label)

    def create_main_panel(self):
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

        # Load and display images from folder
        image_folder = r'C:\Users\ASUS\Desktop\Project Pics\AnaLibano'
        images = self.load_images_from_folder(image_folder)
        row_layout = None
        for i, image_path in enumerate(images, 1):
            if i % 5 == 1:
                # Create a new row for every 5th image
                row_layout = BoxLayout(orientation='horizontal', size_hint=(0.99, None), height='96dp')
                image_display.add_widget(row_layout)

            image = AsyncImage(source=image_path)
            row_layout.add_widget(image)

    def create_button_bar(self):
        button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))

        add_tags_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')

        button_bar.add_widget(add_tags_button)
        button_bar.add_widget(remove_tags_button)
        button_bar.add_widget(search_button)
        button_bar.add_widget(zip_button)
        button_bar.add_widget(rotate_button)

        return button_bar

    def load_images_from_folder(self, folder_path):
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(os.path.join(folder_path, filename))
        return images

PicLib().run()


"""Temos o layout das 3 caixas necessárias +1 classe para colocar cor na label,
os botões das tags estão definidos no entanto
acho que não temos o Save pretendido não sei se é o das tags ou não,
nós temos o do self.filename no ImageCollection,
falta-nos o Zip peço que confirmes sff e falta o Rotation90 degree,
em relação ao bidding das imagens para darem showcase
estava a pensar secalhar em grid?Para ficarem todas juntinhas
sem ocupar diferentes tamanhos no main ficava mais clean
no entanto não se dá para fazer como estou a pensar,
aos botões vou lhes meter colors type HEX ou RGB, é mais universal
 i mean não é preciso fazer a divisão por 255 no entanto é irrelevante"""

"""Outra coisa, deves ter de instalar o sdl12 do kivy,
(pip install "kivy[sdl2]") no terminal """