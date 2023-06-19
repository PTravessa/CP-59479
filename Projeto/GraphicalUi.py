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

default_folder = 'C:/Users/andre/CP/'
#default_folder = r'C:\Users\ASUS\Desktop\Project Pics\AnaLibano'
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
        self.foldername = "/".join(self.image_source.split('\\')[:-1]) 
        self.filename = self.image_source.split('\\')[-1]
        self.cpimage = CPImage(self.filename, self.foldername)

        self.image = Image(source=self.image_source)
        self.add_widget(self.image)

        with self.canvas.before:
            self.frame_color = Color(1, 1, 1, 1)  # White color
            self.frame = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_image_size, pos=self._update_image_pos)
        self.bind(active=self.on_active)

        if self.id in self.selected_images:
            self.frame_color.rgba = (1, 0, 0, 1)        

    def get_date(self):
        return self.cpimage.getDate()

    def rotate(self):
        # im = Image.open(self.getImagefile())
        self.image.rotate(-90, expand=True)
        width, height = self.metadata['dimensions']
        self.image.metadata['dimensions'] = (height, width)
        self.image.reload()

    def remove_tag(self, tag):
        self.cpimage.removeTag(tag)

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
        self.images_per_page =6  #25
        self.page_label = None
        self.addedTags = []
        self.activeTags = []
        self.images = []

        #Buttons, BoxLayouts and labels
        self.collection_tags_button = None
        self.button_bar = None
        self.currentImgFolder = None
        self.okButton = None
        self.cancel_button = None
        self.zip_button = None
        self.rotate_button = None
        self.tag_display = None
        self.rem_tag_button = None
        self.add_tag_img_button = None
        self.dateLabel = None
        self.tagsInImages = set()

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
        self.dateLabel = self.create_date_label()
        self.bottom_row.add_widget(self.dateLabel)
        self.bottom_row_label = Label(text='Tags',color='#94FFDA', font_size=25, size_hint=(0.4, 1))
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
        cur_img_date = ''
        if num_selected_images >= 1:
            lastKey = list(SelectableImage.selected_images.keys())[-1]
            cur_img_date = SelectableImage.selected_images[lastKey].get_date()
            if cur_img_date == '':
                cur_img_date = 'NA'
            else: cur_img_date = cur_img_date[0:10]

        self.dateLabel.text = "Date: " + cur_img_date
        if num_selected_images == 1 and not self.zip_button in self.button_bar.children: #and not self.rotate_button in self.button_bar.children:
            # self.add_zip_and_rot_to_buttonBar()
            self.button_bar.add_widget(self.create_zip_button())
            # self.button_bar.add_widget(self.remove_tags_button)
        if num_selected_images == 1 and not self.rotate_button in self.button_bar.children:
            if self.rem_tag_button not in self.button_bar.children:
                self.create_remTag_button()
                self.button_bar.add_widget(self.rem_tag_button)
            self.button_bar.add_widget(self.create_rotate_button())
        if num_selected_images == 1:
            if self.add_tag_img_button not in self.button_bar.children:
                self.create_addTag_img_button()
                self.button_bar.add_widget(self.add_tag_img_button)        
        
        if num_selected_images > 1:
            if self.rem_tag_button not in self.button_bar.children:
                self.create_remTag_button()
                self.button_bar.add_widget(self.rem_tag_button)
            if self.rotate_button in self.button_bar.children:
                self.button_bar.remove_widget(self.rotate_button)
            if self.add_tag_img_button not in self.button_bar.children:
                self.create_addTag_img_button()
                self.button_bar.add_widget(self.add_tag_img_button) 

        elif num_selected_images <= 0:
            if self.zip_button in self.button_bar.children:
                self.button_bar.remove_widget(self.zip_button)
            if self.rem_tag_button in self.button_bar.children:
                self.button_bar.remove_widget(self.rem_tag_button)
            if self.rotate_button in self.button_bar.children:
                self.button_bar.remove_widget(self.rotate_button)
            if self.add_tag_img_button in self.button_bar.children:
                self.button_bar.remove_widget(self.add_tag_img_button)
            # self.button_bar.remove_widget(self.remove_tags_button)

    def add_zip_and_rot_to_buttonBar(self):
        self.create_zip_button()
        self.rotate_button = self.create_rotate_button()
        self.button_bar.add_widget(self.zip_button)
        self.button_bar.add_widget(self.rotate_button)

    def create_zip_button(self):
        self.zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        self.zip_button.bind(on_press=lambda _, images=SelectableImage.selected_images: self.zip_files_popup(images))
        return self.zip_button
    
    def create_rotate_button(self):
        self.rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')
        self.rotate_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.rotate_image(image))
        return self.rotate_button
    
    def create_remTag_button(self):
        self.rem_tag_button = Button(text='T-', font_size=20, background_color='#94FFDA')
        self.rem_tag_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.rem_tag_page(image))
        return self.rem_tag_button
    
    def rem_tag_page(self, images = SelectableImage.selected_images):
        print("sakdhfdjknkjasnkanfk")
        self.tagsInImages = set()
        cpiImgs = []
        for image in images:
            print(list(images.values())[0].image_source.split("/"))
            filePath = list(images.values())[0].image_source.split("/")[-1]
            folderPath = list(images.values())[0].image_source.split("/")[:-1]
            folderPath = "/".join(folderPath)
            # cpiImgs.append(CPImage(filePath, folderPath))
            tags = CPImage(filePath, folderPath).getTagsList()
            for tag in tags:
                self.tagsInImages.add(tag)
        
        if self.image_display in self.main_panel.children:
            self.main_panel.remove_widget(self.image_display)
        self.button_bar.clear_widgets()
        self.cancel_button = self.get_cancel_button()
        self.button_bar.add_widget(self.cancel_button)
        self.create_tag_display(tagList=list(self.tagsInImages))
        if self.tag_display not in self.main_panel.children:
            # self.tag_display = self.create_tag_display(tagList=list(tagsInImages))
            self.main_panel.add_widget(self.tag_display)
        for layout in self.tag_display.children:
            for tagButton in layout.children:
                print("TagButton = " +str(tagButton))
                tagButton.bind(on_press=lambda _, images=SelectableImage.selected_images: self.rem_tag_image(images, tagButton.text, tagButton))

    def rem_tag_image(self, images, tag, tagButton):
        for key in images.keys():
            selectableImg = images[key]
            selectableImg.remove_tag(tag)
            self.tagsInImages.discard(tag)
            tagButton.unbind(on_press=self.rem_tag_image)

            
            self.create_tag_display()

    def create_addTag_img_button(self):
        self.add_tag_img_button = Button(text='T+', font_size=20, background_color='#94FFDA')
        self.add_tag_img_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.add_tag_img_page(image))
        return self.add_tag_img_button

    def rem_remTagButton(self):
        if self.rem_tag_button in self.button_bar.children:
            self.button_bar.remove_widget(self.rem_tag_button)

    def rem_zipButton(self):
        if self.zip_button in self.button_bar.children:
            self.button_bar.remove_widget(self.zip_button)

    def rem_rotateButton(self):
        if self.rotate_button in self.button_bar.children:
            self.button_bar.remove_widget(self.rotate_button)




    
    def rotate_image(self, image=SelectableImage.selected_images):
        imageId = list(image.values())[0].id
        img_path = list(image.values())[0].image_source
        print("img_path = "+str(img_path))
        original_image = PILImage.open(img_path)
        # original_image.resize([original_image.height, original_image.width])
        rotated_img = original_image.rotate(-90, expand=True)
        width, height = original_image.size

        rotated_img.resize((height, width))
        rotated_img.save(img_path)
        self.images[imageId-1] = img_path
        SelectableImage.selected_images[imageId] = SelectableImage(img_path, id=imageId)
        # SelectableImage.selected_images[imageId].image.rotate()
        SelectableImage.selected_images[imageId].image.reload()
        

        self.update_image_display()


    def zip_files_popup(self, images):
        # Create a popup with a text input for adding tags
        popup_content = BoxLayout(orientation='vertical', padding=10)
        zip_filename = TextInput(multiline=False, hint_text='Enter zip path')
        zip_folder = TextInput(multiline=False, hint_text='Enter full folderPath (write "default" for default)', text='')
        zip_button = Button(text='Ok')
        zip_button.bind(on_press=lambda *args: self.zip_files(images=SelectableImage.selected_images, zip_filename=zip_filename.text, zip_folder=zip_folder.text, popup=popup))
        popup_content.add_widget(zip_filename)
        popup_content.add_widget(zip_folder)
        popup_content.add_widget(zip_button)

        popup = Popup(title='Enter the zip path', content=popup_content, size_hint=(0.4, 0.4))

        popup.open()

    def zip_files(self, images, zip_filename, zip_folder, popup):
        # # Create a ZipFile Object
        if not zip_filename.endswith('.zip'):
            zip_filename += '.zip'
        if zip_folder == 'defaultss':
            zip_folder = default_folder
        zip_path = zip_folder+"/ZippedImageFolder/"+zip_filename 
        if not os.path.isdir(zip_folder+"/ZippedImageFolder/"):
            os.mkdir(zip_folder+"/ZippedImageFolder/")
        with ZipFile(zip_path, 'w') as zip_object:
           # Adding files that need to be zipped
           for imageKey in images:
               images[imageKey].image_source
            #    print("images[imageKey].image_source.split(\"\\\")[1] = " + str(images[imageKey].image_source.split("\\")[1]))
               zip_object.write(images[imageKey].image_source, arcname=images[imageKey].image_source.split("\\")[1])
        popup.dismiss()

    def create_date_label(self):
        self.dateLabel = Label(text="Date: ", size_hint=(0.4, 1))
        return self.dateLabel


    def create_main_panel(self):
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

        self.image_display = image_display

        # Load and display images from folder
        # image_folder = r'C:\Users\ASUS\Desktop\Project Pics\AnaLibano'
        self.image_folder = 'C:/Users/andre/CP/fotos/'
        self.images = self.load_images_from_folder(self.image_folder)
        self.original_images = self.load_images_from_folder(self.image_folder) #Backup images
        self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
        self.update_image_display()

    def create_button_bar(self):
        self.button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))

        self.collection_tags_button = Button(text='T', font_size=20, background_color='#94FFDA')

        self.rem_tag_button = self.create_remTag_button()
        # C3 add_tags_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        self.collection_tags_button.bind(on_press=self.on_add_tags_button)
        # self.remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        self.search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        self.search_button.bind(on_press=self.load_tags)
        # zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        # rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')

        self.button_bar.add_widget(self.collection_tags_button)
        self.button_bar.add_widget(self.rem_tag_button)
        # self.button_bar.add_widget(self.remove_tags_button)

        #This creates a shallow copy, so all changes in ogbuttonbar change buttonbar
        # self.original_button_bar = self.button_bar  # Store the original button bar

        #self.button_bar.add_widget(add_tags_button)
        self.button_bar.add_widget(self.search_button)
        #self.button_bar.add_widget(remove_tags_button)
        #self.button_bar.add_widget(zip_button)
        #self.button_bar.add_widget(rotate_button)

        return self.button_bar
    
    def rem_tag_from_image_button(self):
        self.rem_tag_image = Button(text='T-', font_size=20, background_color='#94FFDA')
        self.search_button.bind(on_press=self.load_tags)
    
    def ok_button(self):
        self.okButton = Button(text="OK", font_size=20, background_color="#94FFDA")
        self.okButton.bind(on_press=self.load_scene_w_tags)
        return self.okButton        

    def load_tags(self, instance):
        self.main_panel.clear_widgets()
        self.button_bar.clear_widgets()

        self.okButton = self.ok_button()
        self.button_bar.add_widget(self.okButton)

        # self.activeTags = []
        # self.images = copy.deepcopy(self.original_images)
        self.addTags_to_main_button = Button(text="<", font_size=20, background_color="#94FFDA")
        self.addTags_to_main_button.bind(on_press=self.on_cancel_tags_button)
        self.button_bar.add_widget(self.addTags_to_main_button)

        self.tag_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))
        self.main_panel.add_widget(self.button_bar)
        self.main_panel.add_widget(self.tag_display)
        self.bottom_row.remove_widget(self.bottom_row_label)


        self.main_panel.spacing = 10
        for tagName in self.addedTags:
            b = Button(text=tagName, font_size=20, background_color="#94FFDA", size_hint=(0.1, 0.1))
            b.bind(on_press=lambda _, tag=tagName: self.add_active_tag(tag))
            self.tag_display.add_widget(b)

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
        self.main_panel.remove_widget(self.tag_display)
        self.main_panel.add_widget(self.image_display)


        image_names = self.get_image_names(self.image_folder)
        imagesWithTags = list()
        if len(self.activeTags) >= 1:
            for image in image_names:
                cpimage = CPImage(image, self.image_folder)
                for tag in self.activeTags:
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


    def search_button_func(self):
        search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        search_button.bind(on_press=self.load_tags)
        return search_button

    def load_images_from_folder(self, folder_path): #Full path of image file
        for filename in os.listdir(folder_path):
            fullPath = os.path.join(folder_path, filename)
            if filename.endswith('.png') or filename.endswith('.jpg'):
                self.images.append(fullPath)
            elif os.path.isdir(fullPath):
                self.load_images_from_folder(fullPath)
        return self.images
    
    def get_image_names(self, folder_path): #Name of image file
        images = []
        for filename in os.listdir(folder_path):
            fullPath = os.path.join(folder_path, filename)
            if filename.endswith('.png') or filename.endswith('.jpg'):
                images.append(filename)
            elif os.path.isdir(fullPath):
                self.get_image_names(fullPath)
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

                ####Testar
                # Randomly select an image
                # random_image = random.choice(self.images)

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

    def get_cancel_button(self):
        self.cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')
        self.cancel_button.bind(on_press=self.on_cancel_tags_button)
        return self.cancel_button

    def on_add_tags_button1(self, instance):
        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        #delete_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        self.cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        #delete_button.bind(on_press=self.on_del_tags_button)
        self.cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        #self.button_bar.add_widget(delete_button)
        self.button_bar.add_widget(self.cancel_button)

        # Remove the image display
        self.main_panel.remove_widget(self.image_display)
        self.tag_display = self.create_tag_display(tagList=self.addedTags)
        if self.tag_display not in self.main_panel.children:
            self.main_panel.add_widget(self.tag_display)

    def on_add_tags_button(self, instance):
        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        #delete_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        #delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        #self.button_bar.add_widget(delete_button)
        self.button_bar.add_widget(cancel_button)

        # Remove the image display
        self.main_panel.remove_widget(self.image_display)
        #Get tags of each img
        # allTagsInImgs = set()
        # for img in SelectableImage.selected_images:
        #     print("img.values() +")
        #     filePath = list(img.values())[0].image_source.split("/")[-1]
        #     folderPath = list(img.values())[0].image_source.split("/")[:-1]
        #     folderPath = "/".join(folderPath)
        #     # cpiImgs.append(CPImage(filePath, folderPath))
        #     tagL = CPImage(filePath, folderPath).getTagsList()
        #     for tag in tagL:
        #         allTagsInImgs.add(tag)
        allTagsInImgs = list(self.addedTags)

        self.tag_display = self.create_tag_display(allTagsInImgs)
        if self.tag_display not in self.main_panel.children:
            self.main_panel.add_widget(self.tag_display)

    def create_tag_display(self, tagList):

        self.tag_display = BoxLayout(orientation='horizontal', size_hint=(0.6, 1), padding=[10,10,10,10], spacing=10)
        tag_display1 = BoxLayout(orientation='vertical', size_hint=(0.6, 1), padding=[10,10,10,10], spacing=10)
        colN = 3
        subDispN = len(tagList)//colN +1

        i = 0
        for x in range(subDispN):
            i = (x+1)*colN
            print("x = "+str(x))

            if i % colN == 0:
                tag_display1 = BoxLayout(orientation='vertical', size_hint=(0.6, 1), padding=[10,10,10,10], spacing=10)
                for i1 in range(colN):
                    print("i1 = "+str(i1))
                    print("x = "+str(x))
                    if (x * colN + i1)<= len(tagList) -1:
                        b = Button(text=tagList[x * colN + i1], font_size=20, background_color="#94FFDA", size_hint=(0.3, 0.3))
                        tag_display1.add_widget(b)
                    print("x * colN + i1 = "+str(x * colN + i1))
                    print("tag_display1 "+ str(tag_display1))
                self.tag_display.add_widget(tag_display1)
                print("tag_display "+ str(self.tag_display))

        return self.tag_display

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
        save_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        #delete_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        #delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        #self.button_bar.add_widget(delete_button)
        self.button_bar.add_widget(cancel_button)

    def on_del_tags_button(self, instance):
        # Perform actions when the "Save" button is pressed
        print("Delete Tag button pressed")

        # Create a popup with a text input for adding tags
        popup_content = BoxLayout(orientation='vertical', padding=10)
        tag_input = TextInput(multiline=False, hint_text='Tags to remove')
        add_button = Button(text='Delete')

        popup_content.add_widget(tag_input)
        popup_content.add_widget(add_button)

        popup = Popup(title='Remove Tags', content=popup_content, size_hint=(0.4, 0.4))
        add_button.bind(on_press=lambda *args: self.del_tag(tag_input.text, popup))
        popup.open()

        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        # Create the new buttons
        save_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        # delete_button = Button(text='-T', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        # Bind the new button actions
        save_button.bind(on_press=self.on_save_tags_button)
        # delete_button.bind(on_press=self.on_del_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        # Add the new buttons to the button bar
        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(self.rem_tag_button)
        self.button_bar.add_widget(cancel_button)

    def del_tag(self, tag, popup):
        if tag not in self.addedTags:
            return
        self.addedTags.remove(tag)
        print(f"Tags: {tag}")
        print(self.addedTags)
        popup.dismiss()        

    def on_cancel_tags_button(self, instance):
        # Perform actions when the "Cancel" button is pressed
        print("Cancel button pressed")

        # # Restore the original button bar
        # # collection_tags_button = Button(text='T', font_size=20, background_color='#94FFDA')
        # # collection_tags_button.bind(on_press=self.on_add_tags_button)
        # remove_tags_button = Button(text='-T', font_size=20, background_color='#94FFDA')

        self.main_panel.remove_widget(self.tag_display)
        search_button = self.search_button_func()
        self.button_bar.size_hint = (0.1, 1)
        self.button_bar.clear_widgets()
        self.button_bar.add_widget(self.collection_tags_button)
        # self.button_bar.add_widget(self.rem_tag_button)
        self.button_bar.add_widget(search_button)
        self.update_selected_images_label()
        self.main_panel.add_widget(self.image_display)
        if self.tag_display in self.main_panel.children:
            self.main_panel.remove_widget(self.tag_display)
        

    def add_tags(self, tags, popup):
        # Perform actions to add tags to selected images
        addedTagsSet = set(self.addedTags)

        addedTagsSet.add(tags)
        self.addedTags = list(addedTagsSet)
        print(f"Tags: {tags}")
        print(self.addedTags)
        if self.tag_display in self.main_panel.children:
            self.main_panel.remove_widget(self.tag_display)
        self.tag_display = self.create_tag_display(tagList=self.addedTags)
        self.main_panel.add_widget(self.tag_display)
        popup.dismiss()

PicLib().run()
