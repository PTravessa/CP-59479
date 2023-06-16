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

#Imagens
class SelectableImage(CheckBox, ButtonBehavior):
    selected_images = []

    def __init__(self, image_source, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''  # Remove default background
        self.group = 'images'
        self.image_source = image_source

        self.image = Image(source=self.image_source)
        self.add_widget(self.image)

        with self.canvas.before:
            self.frame_color = Color(1, 1, 1, 1)  # White color
            self.frame = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_image_size, pos=self._update_image_pos)
        self.bind(active=self.on_active)

    def _update_image_size(self, *args):
        self.image.size = self.size
        self.frame.size = self.size

    def _update_image_pos(self, *args):
        self.image.pos = self.pos
        self.frame.pos = self.pos

    def on_active(self, instance, value):
        if value:
            self.frame_color.rgba = (1, 0, 0, 1)  # Red color when active
            if self not in self.selected_images:
                self.selected_images.append(self)  # Add self to selected_images list
        else:
            self.frame_color.rgba = (1, 1, 1, 1)  # White color when inactive
            if self in self.selected_images:
                self.selected_images.remove(self)  # Remove self from selected_images list

        # Call the update_selected_images_label method from PicLib
        app = App.get_running_app()
        app.update_selected_images_label()


class PicLib(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_row = None  # BoxLayout
        self.bottom_row = None  # BoxLayout
        self.main_panel = None  # BoxLayout
        self.page_number = 1
        self.total_pages = 1
        self.images_per_page = 25
        self.page_label = None

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

        prev_button = Button(text='<', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        next_button = Button(text='>', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        prev_button.bind(on_press=self.go_to_previous_page)
        next_button.bind(on_press=self.go_to_next_page)
        self.bottom_row.add_widget(prev_button)

        self.page_label = Label(text='Page 1', font_size=18, size_hint=(0.1, 0.98))
        self.bottom_row.add_widget(self.page_label)

        self.selected_images_label = Label(text='Selected: 0', font_size=11, size_hint=(0.1, 0.99))
        self.bottom_row.add_widget(self.selected_images_label)

        self.bottom_row.add_widget(next_button)

        return self.bottom_row

    def update_selected_images_label(self):
        num_selected_images = len(set(SelectableImage.selected_images))
        self.selected_images_label.text = f'Selected: {num_selected_images}'


    def create_main_panel(self):
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

        self.image_display = image_display

        # Load and display images from folder
        image_folder = r'C:\Users\ASUS\Desktop\Project Pics\AnaLibano'
        self.images = self.load_images_from_folder(image_folder)
        self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
        self.update_image_display()

    def create_button_bar(self):
        self.button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))

        add_tags_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        add_tags_button.bind(on_press=self.on_add_tags_button)
        remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')

        self.original_button_bar = self.button_bar  # Store the original button bar

        self.button_bar.add_widget(add_tags_button)
        self.button_bar.add_widget(remove_tags_button)
        self.button_bar.add_widget(search_button)
        self.button_bar.add_widget(zip_button)
        self.button_bar.add_widget(rotate_button)

        return self.button_bar

    def load_images_from_folder(self, folder_path):
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(os.path.join(folder_path, filename))
        return images

    def update_image_display(self):
        self.image_display.clear_widgets()

        start_index = (self.page_number - 1) * self.images_per_page
        end_index = self.page_number * self.images_per_page
        images_to_display = self.images[start_index:end_index]

        rows = len(images_to_display) // 5  # Number of rows to create
        if len(images_to_display) % 5 != 0:
            rows += 1

        for i in range(rows):
            row_images = images_to_display[i * 5:(i + 1) * 5]

            row_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
            for image_path in row_images:
                image = SelectableImage(image_source=image_path)
                image.bind(on_release=self.on_image_selected)
                row_layout.add_widget(image)

            self.image_display.add_widget(row_layout)
        self.page_label.text = f'Page {self.page_number}'

    def on_image_selected(self, instance):
        # Perform actions when an image is selected
        print(f"Selected image: {instance.image_source}")

    def go_to_previous_page(self, instance):
        if self.page_number > 1:
            self.page_number -= 1
            self.update_image_display()

    def go_to_next_page(self, instance):
        if self.page_number < self.total_pages:
            self.page_number += 1
            self.update_image_display()

    def on_add_tags_button(self, instance):
        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='Ok', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(cancel_button)

    def on_save_tags_button(self, instance):
        # Perform actions when the "Save" button is pressed
        print("Save Tag button pressed")

        # Create a popup with a text input for adding tags
        popup_content = BoxLayout(orientation='vertical', padding=10)
        tag_input = TextInput(multiline=False, hint_text='Enter tags')
        add_button = Button(text='Add')

        popup_content.add_widget(tag_input)
        popup_content.add_widget(add_button)

        popup = Popup(title='Add Tags', content=popup_content, size_hint=(0.4, 0.4))
        add_button.bind(on_press=lambda *args: self.add_tags(tag_input.text, popup))
        popup.open()

        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='Ok', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(cancel_button)

    def on_cancel_tags_button(self, instance):
        # Perform actions when the "Cancel" button is pressed
        print("Cancel button pressed")

        # Restore the original button bar
        self.button_bar.clear_widgets()
        self.button_bar.add_widget(self.original_button_bar)

    def add_tags(self, tags, popup):
        # Perform actions to add tags to selected images
        print(f"Tags: {tags}")
        popup.dismiss()

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
"""+T está a criar o popup para inserir o text input da nova tag a criar e 
leva nos a um novo layout, ainda estou a tentar perceber como integrar os diferentes layouts
 visto que não estou a conseguir colocar widgets parentais e assim tenho mesmo de criar diferetnes layouts A,B,C,D
 a seleção de imagem continua a ser só possivel selecioanr 1,no entanto ainda não integrei o nosso PicLib 
 nem as collections que temos como output estou a utilizar apenas as imagens todas numa pasta porque
 queria testar a navegação entre paginas. Pata tal na utilização para adicionar as tags o novo layout funciona 
 até ao botão ok que aciona o popup para dar add à Tag mas o de voltar da crash a app"""
"""Outra coisa, deves ter de instalar o sdl12 do kivy,
(pip install "kivy[sdl2]") no terminal """