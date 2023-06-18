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

import math

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


class PicLib(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_row = None  # BoxLayout
        self.bottom_row = None  # BoxLayout
        self.main_panel = None  # BoxLayout
        self.image_display = None
        self.page_number = 1
        self.total_pages = 1
        self.images_per_page = 6
        self.page_label = None
        self.addedTags = []
        self.activeTags = []

        self.currentImgFolder = None

    def build(self):
        self.create_top_row()
        self.create_bottom_row()
        self.create_main_panel()

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.top_row)
        main_layout.add_widget(self.main_panel)
        main_layout.add_widget(self.bottom_row)

        return main_layout

    def create_top_row(self): #Toprow with a label, and a widget with it inside
        self.top_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_row_label = Label(text='PicLib', font_size=40)
        self.top_row.add_widget(top_row_label)

    def create_bottom_row(self): #Has label, functional~ prev next buttons, 
        self.bottom_row = BrownBoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.bottom_row_label = Label(text='Tags',color='#94FFDA', font_size=25)
        self.bottom_row.add_widget(self.bottom_row_label)

        prev_button = Button(text='<', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        next_button = Button(text='>', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        prev_button.bind(on_press=self.go_to_previous_page)
        next_button.bind(on_press=self.go_to_next_page)
        self.bottom_row.add_widget(prev_button)

        self.page_label = Label(text='Page 1', font_size=18, size_hint=(0.1, 0.98))
        self.bottom_row.add_widget(self.page_label)
        self.selected_images_label = Label(text='Selected: 0', font_size=11, size_hint=(0.13, 1))
        self.bottom_row.add_widget(self.selected_images_label)

        self.bottom_row.add_widget(next_button)

        return self.bottom_row
    
    def add_pageIndex_prev_next_to_bottomRow(self):
        prev_button = Button(text='<', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        next_button = Button(text='>', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        prev_button.bind(on_press=self.go_to_previous_page)
        next_button.bind(on_press=self.go_to_next_page)
        self.bottom_row.add_widget(prev_button)

        self.page_label = Label(text='Page 1', font_size=18, size_hint=(0.1, 0.98))
        self.bottom_row.add_widget(self.page_label)
        self.selected_images_label = Label(text='Selected: 0', font_size=11, size_hint=(0.13, 1))
        self.bottom_row.add_widget(self.selected_images_label)

        self.bottom_row.add_widget(next_button)

    def update_selected_images_label(self):
        num_selected_images = len((SelectableImage.selected_images))
        self.selected_images_label.text = f'Selected: {num_selected_images}'


    def create_main_panel(self):
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

        self.image_display = image_display

        # Load and display images from folder
        # image_folder = r'C:\Users\ASUS\Desktop\Project Pics\AnaLibano'
        self.image_folder = 'C:/Users/andre/CP/fotos/AnaLibano'
        self.images = self.load_images_from_folder(self.image_folder)
        self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
        self.update_image_display()

    def create_button_bar(self):
        self.button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))

        collection_tags_button = Button(text='T', font_size=20, background_color='#94FFDA')
        # C3 add_tags_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        collection_tags_button.bind(on_press=self.on_add_tags_button)
        remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        search_button.bind(on_press=self.load_tags)
        zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')

        self.button_bar.add_widget(collection_tags_button)
        self.button_bar.add_widget(remove_tags_button)

        #This creates a shallow copy, so all changes in ogbuttonbar change buttonbar
        # self.original_button_bar = self.button_bar  # Store the original button bar

        #self.button_bar.add_widget(add_tags_button)
        self.button_bar.add_widget(search_button)
        #self.button_bar.add_widget(remove_tags_button)
        #self.button_bar.add_widget(zip_button)
        #self.button_bar.add_widget(rotate_button)

        return self.button_bar
    
    def load_tags(self, instance):
        self.main_panel.clear_widgets()
        self.button_bar.clear_widgets()

        okButton = Button(text="OK", font_size=20, background_color="#94FFDA")
        okButton.bind(on_press=self.load_scene_w_tags)
        self.button_bar.add_widget(okButton)

        tag_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
        self.main_panel.add_widget(self.button_bar)
        self.main_panel.add_widget(tag_display)
        self.bottom_row.remove_widget(self.bottom_row_label)

        self.main_panel.spacing = 10
        for tagName in self.addedTags:
            b = Button(text=tagName, font_size=20, background_color="#94FFDA", size_hint=(0.1, 0.1))
            b.bind(on_press=lambda _, tag=tagName: self.add_active_tag(tag))
            tag_display.add_widget(b)

    def add_active_tag(self, tag):
        if tag not in self.activeTags:
            self.activeTags.append(tag)

    def load_scene_w_tags(self, instance):
        self.main_panel.clear_widgets()
        self.button_bar.clear_widgets()
        self.button_bar = self.create_button_bar()
        self.main_panel.add_widget(self.button_bar)

        tag_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
        # self.main_panel.add_widget(self.button_bar)
        self.main_panel.add_widget(self.image_display)


        image_names = self.get_image_names(self.image_folder)
        imagesWithTags = list()
        if len(self.addedTags) >= 1:
            for image in image_names:
                cpimage = CPImage(image, self.image_folder)
                for tag in self.addedTags:
                    if cpimage.hasTag(tag):
                        imagesWithTags.append(self.image_folder+"/"+image)
                        break
        else:
            for image in image_names:
                imagesWithTags.append(self.image_folder+"/"+image)
        self.images = imagesWithTags
        print("Self.images= "+str(self.images))
        
        self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
        self.update_image_display()
        # self.main_panel.add_widget(self.image_display)
        self.bottom_row.clear_widgets()
        self.bottom_row_label = Label(text="Tags: "+str(self.activeTags)[1:-1].replace("'", ""))
        self.bottom_row.add_widget(self.bottom_row_label)
        self.add_pageIndex_prev_next_to_bottomRow()

    def create_empty_main_panel(self, instance):
        self.main_panel.clear_widgets()
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        self.image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(self.image_display)
        return self.main_panel


    def search_button(self):
        search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        search_button.bind(on_press=self.load_tags)
        return search_button

    def load_images_from_folder(self, folder_path): #Full path of image file
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(os.path.join(folder_path, filename))
        return images
    
    def get_image_names(self, folder_path): #Name of image file
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(filename)
        return images

    def update_image_display(self):
        self.image_display.clear_widgets()

        start_index = (self.page_number - 1) * self.images_per_page
        end_index = self.page_number * self.images_per_page
        images_to_display = self.images[start_index:end_index]

        rows = len(images_to_display) // 5  # Number of rows to create
        if len(images_to_display) % 5 != 0:
            rows += 1

        image_index = start_index
        for i in range(rows):
            row_images = images_to_display[i * 5:(i + 1) * 5]

            row_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
            for image_path in row_images:
                image_index += 1
                image = SelectableImage(image_source=image_path, id=image_index)
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
        save_button = Button(text='T+', font_size=20, background_color='#94FFDA')
        delete_button = Button(text='T-', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(delete_button)
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
        save_button = Button(text='T+', font_size=20, background_color='#94FFDA')
        delete_button = Button(text='T-', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(delete_button)
        self.button_bar.add_widget(cancel_button)

    def on_del_tags_button(self, instance):
        # Perform actions when the "Save" button is pressed
        print("Delete Tag button pressed")

        # Create a popup with a text input for adding tags
        popup_content = BoxLayout(orientation='vertical', padding=10)
        tag_input = TextInput(multiline=False, hint_text='Delete tags')
        add_button = Button(text='Delete')

        popup_content.add_widget(tag_input)
        popup_content.add_widget(add_button)

        popup = Popup(title='Add Tags', content=popup_content, size_hint=(0.4, 0.4))
        add_button.bind(on_press=lambda *args: self.del_tag(tag_input.text, popup))
        popup.open()

        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='T+', font_size=20, background_color='#94FFDA')
        delete_button = Button(text='T-', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(delete_button)
        self.button_bar.add_widget(cancel_button)

    def del_tag(self, tag, popup):
        self.addedTags.remove(tag)
        print(f"Tags: {tag}")
        print(self.addedTags)
        popup.dismiss()        

    def on_cancel_tags_button(self, instance):
        # Perform actions when the "Cancel" button is pressed
        print("Cancel button pressed")

        # Restore the original button bar
        collection_tags_button = Button(text='T', font_size=20, background_color='#94FFDA')
        collection_tags_button.bind(on_press=self.on_add_tags_button)
        remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')

        search_button = self.search_button()
        zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')
        self.button_bar.clear_widgets()
        self.button_bar.add_widget(collection_tags_button)
        self.button_bar.add_widget(remove_tags_button)
        self.button_bar.add_widget(search_button)
        self.button_bar.add_widget(zip_button)
        self.button_bar.add_widget(rotate_button)
        

    def add_tags(self, tags, popup):
        # Perform actions to add tags to selected images
        self.addedTags.append(tags)
        print(f"Tags: {tags}")
        print(self.addedTags)
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