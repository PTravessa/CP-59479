"""Projeto PicLib
Faculdade de Ciências da Universidade de Lisboa
Departamento de Informática
Collabs: FC60919 (Jens Andreas) and FC59479 (Pedro Travessa)
Link to github: https://github.com/PTravessa/CP-59479/tree/main/Projeto
"""
from PicLib_Phase1 import * 
from kivy.app import App
from kivy.core.window import Window
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
from BrownBoxLayout import *
from SelectableImage import *
from FolderSelectionPopup import *
import random
import math
import copy
import datetime

class PicLib(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = None
        self.top_row = None  # BoxLayout
        self.bottom_row = None  # BoxLayout
        self.main_panel = None  # BoxLayout
        self.image_display = None
        self.page_number = 1
        self.total_pages = 1
        self.images_per_page =6  #Default value
        self.page_label = None
        self.addedTags = []
        self.activeTags = []
        self.images = []
        self.imageNames = []

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
        self.reset_active_tags_button = None
        self.tagsInImages = set()
        self.change_button = None
        self.loadColButton = None
        self.Userselectbutton = None

    def build(self):
        self.create_top_row()
        self.create_bottom_row()
        self.create_main_panel()

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.top_row)
        main_layout.add_widget(self.main_panel)
        main_layout.add_widget(self.bottom_row)

        Window.bind(on_request_close = self.on_request_close)

        return main_layout
    
    def on_request_close(self, btn):
        """
        This function is called when the user clicks close button in window
        """
        content = BoxLayout(orientation = 'horizontal', spacing = '5')
        popup = Popup(title='Save Collection before leaving?', content = content, size_hint=(None, None), size=(600, 300))
        btn2 = Button(text='Yes', size_hint=(1, 0.25), on_release = self.saveImgCol)
        btn1 = Button(text='No', size_hint=(1, 0.25), on_release = self.stop)
        
        content.add_widget(btn2)
        content.add_widget(btn1)

        popup.open()
        return True

    def create_top_row(self):
        """Create the top row of the UI.
        Creates a BoxLayout with horizontal orientation and adds a label
        with the title of the APP "PicLib" to it.
        """
        self.top_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_row_label = Label(text='PicLib', font_size=40)
        self.top_row.add_widget(top_row_label)

    def create_bottom_row(self):
        """
        Creates bottom row of UI (with page numbering etc.)
        """ 
        self.bottom_row = BrownBoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.bottom_row_label = Label(text="Tags: ", color='#94FFDA', font_size=25, size_hint=(0.4, 1))
        # self.update_bottom_row_label()
        self.updateBottomLabelTags()
        self.bottom_row.add_widget(self.bottom_row_label)

        prev_button = Button(text='\n<\n', font_size=40,background_color='#94FFDA', size_hint=(0.05, 0.99))
        next_button = Button(text='\n>\n', font_size=40,background_color='#94FFDA', size_hint=(0.05, 0.99))
        prev_button.bind(on_press=self.go_to_previous_page)
        next_button.bind(on_press=self.go_to_next_page)
        self.bottom_row.add_widget(prev_button)

        self.page_label = Label(text='Page 1', font_size=18, size_hint=(0.1, 0.98))
        self.bottom_row.add_widget(self.page_label)
        self.selected_images_label = Label(text='Selected: 0', font_size=12, size_hint=(0.10, 1))
        self.bottom_row.add_widget(self.selected_images_label)

        self.bottom_row.add_widget(next_button)

        # Button to change images_per_page value
        self.change_button = Button(text = " Change \n  Image \n Display", font_size=12,background_color='#94FFDA', size_hint=(0.085,0.99))
        self.change_button.bind(on_press=self.change_images_per_page)
        self.bottom_row.add_widget(self.change_button)

        self.dateLabel = self.create_date_label()
        self.bottom_row.add_widget(self.dateLabel, index=-1)
        self.create_loadColButton()
        self.bottom_row.add_widget(self.loadColButton)

        return self.bottom_row
    
    def create_loadColButton(self):
        """Create a button to load the previous collection.
        Creates a Button with the text "Load previous collection"
        and sets up the event binding to the loadCol1 method.
        """
        self.loadColButton = Button(text="     Load\n  previous\n collection",font_size=12,size_hint=(0.10,0.99))
        self.loadColButton.bind(on_press=self.loadCol1)
        return self.loadColButton

    def create_change_button(self):
        """Create a button to change the image display.
        Creates a Button widget with the text "Change Image Display" and sets up the
        event binding to the change_images_per_page method.
        """
        # Button to change images_per_page value
        self.change_button = Button(text = " Change \n  Image \n Display", font_size=12,background_color='#94FFDA', size_hint=(0.085,0.99))
        self.change_button.bind(on_press=self.change_images_per_page)
        return self.change_button
    
    def create_main_panel(self):
        """Create the main panel layout.
        Creates a box layout widget that serves as the main panel of the application.
        It consists of a button bar and an image display. The button bar contains various buttons for interacting with
        the images, is initially set to show a placeholder button indicating that no folder is selected.
        The main panel is displayed horizontally.
        """
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

        self.image_display = image_display

        self.Userselectbutton = Button(text='\n\n\n\n\n                                         Empty Panel'
                                  +'\n\nPlease Select a Folder with the Corresponding Images to Load'
                                  + '\n\n\n\n\n\n\n                           Double Click to Open a Folder',
                                  background_color=(0, 0, 0, 1)
        )
        self.Userselectbutton.bind(on_release=self.open_folder_selection_popup)
        image_display.add_widget(self.Userselectbutton)

    def create_button_bar(self):
        """Create the button bar layout.
        Creates a vertical box layout widget that serves as the button bar.
        The button bar contains various buttons for interacting with the images, such as:
        adding tags, searching for images, and removing tags.
        The layout is initially empty, and buttons are added dynamically based on the selected images.
        """
        self.button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))
        self.collection_tags_button = Button(text='T', font_size=20, background_color='#94FFDA')

        self.rem_tag_button = self.create_remTag_button()
        self.collection_tags_button.bind(on_press=self.on_add_tags_button)
        self.search_button = self.create_search_button()

        self.button_bar.add_widget(self.collection_tags_button)
        self.button_bar.add_widget(self.search_button)
        return self.button_bar

    def add_pageIndex_prev_next_to_bottomRow(self):
        """
        Add page number and buttons for going back/forward in pages list
        """
        prev_button = Button(text='<', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        next_button = Button(text='>', font_size=20,background_color='#94FFDA', size_hint=(0.1, 0.99))
        prev_button.bind(on_press=self.go_to_previous_page)
        next_button.bind(on_press=self.go_to_next_page)
        self.bottom_row.add_widget(prev_button)

        self.page_label = Label(text='Page 1', font_size=18, size_hint=(0.1, 0.98))
        self.bottom_row.add_widget(self.page_label)
        self.selected_images_label = Label(text='Selected: 0', font_size=12, size_hint=(0.10, 1))
        self.bottom_row.add_widget(self.selected_images_label)

        self.bottom_row.add_widget(next_button)

    def change_images_per_page(self, instance):
        """Change the number of images to display per page.
        Creates a popup with a text input field for the user to enter the new value
        of images_per_page. When the user clicks the "Save" button, the new value is updated and
        the image display is updated accordingly.
        """
        # Create a popup to get the new value
        content = BoxLayout(orientation='vertical', spacing=10)
        input_text = TextInput(text=str(self.images_per_page), multiline=False, hint_text='Enter Number of Images to Display')
        save_button = Button(text='Save')

        def save_value(instance):
            # Update the images_per_page value with the new input
            try:
                new_value = int(input_text.text)
                if new_value > 0:
                    self.images_per_page = new_value
                    print(f"images_per_page changed to {self.images_per_page}")
                    self.update_image_display()
                else:
                    print("Invalid value. The range should be bigger than 1.")
            except ValueError:
                print("Invalid value. Please enter a valid integer.")

            popup.dismiss()

        save_button.bind(on_press=save_value)
        content.add_widget(input_text)
        content.add_widget(save_button)

        popup = Popup(title='Change Images Per Page', content=content, size_hint=(0.6, 0.4))
        popup.open()

    def update_selected_images_label(self):
        """Update the label and buttons based on the number of selected images.
        Updates the label and buttons in the button_bar based on the number of
        selected images. It adds the change_button to the bottom_row if it's not already there.
        It updates the dateLabel, selected_images_label, and cur_img_date based on the selected
        images. It also manages the visibility of the zip_button, rotate_button, rem_tag_button,
        and add_tag_img_button based on the number of selected images.
        """
        if self.change_button not in self.bottom_row.children:
            self.bottom_row.add_widget(self.change_button)

        self.bottom_row.remove_widget(self.dateLabel)
        self.dateLabel=self.create_date_label() #Updating dateLabel
        self.bottom_row.add_widget(self.dateLabel, index=-1)
        num_selected_images = len((SelectableImage.selected_images))
        self.selected_images_label.text = f'Selected: {num_selected_images}'
        cur_img_date = ''

        self.updateBottomLabelTags()

        if num_selected_images >= 1:
            lastKey = list(SelectableImage.selected_images.keys())[-1]
            cur_img_date = SelectableImage.selected_images[lastKey].get_date()
            if cur_img_date == '':
                cur_img_date = 'NA'
            else: cur_img_date = cur_img_date[0:10]

        if num_selected_images == 1:
            if not self.bottom_row_label in self.bottom_row.children:
                self.bottom_row.add_widget(self.bottom_row_label, index=-1)
        
        if num_selected_images == 1 and not self.zip_button in self.button_bar.children: #and not self.rotate_button in self.button_bar.children:

            if not self.zip_button in self.button_bar.children:
                self.button_bar.add_widget(self.create_zip_button())
            if not self.rotate_button in self.button_bar.children:
                if self.rem_tag_button not in self.button_bar.children:
                    self.create_remTag_button()
                    self.button_bar.add_widget(self.rem_tag_button)
                self.button_bar.add_widget(self.create_rotate_button())
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

    def updateBottomLabelTags(self):
        """Update the label with the selected image tags.
        Retrieves the tags from the selected image(s) and updates the bottom_row_label
        with the tags. It returns the updated bottom_row_label.
        """
        tags = []
        if SelectableImage.selected_images != [] and len(SelectableImage.selected_images) == 1:
            for key in SelectableImage.selected_images.keys():
                tags = SelectableImage.selected_images[key].get_all_tags()
                # allTags = allTags.intersection(tags)
        s = str(tags)
        s = "Tags: " + s

        self.bottom_row_label.text = s
        return self.bottom_row_label 

    def add_zip_and_rot_to_buttonBar(self):
        """Add the zip and rotate buttons to the button bar.
        Creates the zip button and rotate button, and adds them to the button bar.
        """
        self.create_zip_button()
        self.create_rotate_button()
        self.button_bar.add_widget(self.zip_button)
        self.button_bar.add_widget(self.rotate_button)

    def create_zip_button(self):
        """Create a zip button.
        Creates a button with the label "Zip" and sets the font size and background color.
        It also binds the button press event to the `zip_files_popup` method, passing the selected images.
        """
        self.zip_button = Button(text='Zip', font_size=20, background_color='#94FFDA')
        self.zip_button.bind(on_press=lambda _, images=SelectableImage.selected_images: self.zip_files_popup(images))
        return self.zip_button
    
    def create_rotate_button(self):
        """Create a rotate button.
        Creates a button with the label "R90°" and sets the font size and background color.
        It also binds the button press event to the `rotate_image` method, passing the selected image.
        """

        self.rotate_button = Button(text='R90°', font_size=20, background_color='#94FFDA')
        self.rotate_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.rotate_image(image))
        return self.rotate_button
    
    def create_remTag_button(self):
        """Create a remove tag button.
        Creates a button with the label "T-" and sets the font size and background color.
        It also binds the button press event to the `rem_tag_page` method, passing the selected image.
        """
        self.rem_tag_button = Button(text='T-', font_size=20, background_color='#94FFDA')
        self.rem_tag_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.rem_tag_page(image))
        return self.rem_tag_button
    
    def rem_tag_page(self, images = SelectableImage.selected_images):
        """Remove tag from images.
        Removes a tag from the selected images. It retrieves the tags associated with each image
        and creates a set of unique tags. Then, it creates a tag display and adds it to the main panel.
        Each tag button in the display is bound to the `rem_tag_image` method to remove the corresponding tag
        from the selected images.
        """
        self.tagsInImages = set()
        cpiImgs = []

        listOfSetsOfTags = []
        for key in images.keys():
            filePath = list(images[key].image_source.split("/"))[-1]
            folderPath = list(images[key].image_source.split("/"))[:-1]
            folderPath = "/".join(folderPath)
            tags = CPImage(filePath, folderPath).getTagsList()
            temp = set()
            for tag in tags:
                self.tagsInImages.add(tag)
                temp.add(tag)
            listOfSetsOfTags.append(temp)

            i = 0
            temp = listOfSetsOfTags[0]
            if len(listOfSetsOfTags) > 1:
                while i < len(listOfSetsOfTags)-1:
                    temp = temp.intersection(listOfSetsOfTags[i+1])
                    i += 1
        self.tagsInImages = temp
        print("self.tagsInImages = "+str(self.tagsInImages))
        
        if self.image_display in self.main_panel.children:
            self.main_panel.remove_widget(self.image_display)
        self.button_bar.clear_widgets()
        self.cancel_button = self.get_cancel_button()
        self.button_bar.add_widget(self.cancel_button)
        self.create_tag_display(tagList=list(self.tagsInImages))
        if self.tag_display not in self.main_panel.children:
            self.main_panel.add_widget(self.tag_display)
        for layout in self.tag_display.children:
            for tagButton in layout.children:
                tag = tagButton.text  # Capture the current value of tagButton.text

                # Define a helper function with a default argument capturing the current tag value
                def on_press_callback(_, images=images, tagButton=tagButton, tag=tag):
                    self.rem_tag_image(images, tag, tagButton)

                tagButton.bind(on_press=on_press_callback)  # Bind the helper function

    def rem_tag_image(self, images, tag, tagButton):
        """Remove a specific tag from the selected images.
        Removes the specified tag from each selected image. It also updates the `tagsInImages`
        set by discarding the removed tag. Finally, it refreshes the tag display by creating a new tag display
        with the updated set of tags.
        """
        for key in images.keys():
            selectableImg = images[key]
            print("tag: "+str(tag))
            selectableImg.remove_tag(tag)
            self.tagsInImages.discard(tag)
            print("tagsInImages discarded tag: "+str(tag))
            tagButton.unbind(on_press=self.rem_tag_image)

        if self.tag_display in self.main_panel.children:
            self.main_panel.remove_widget(self.tag_display)
        self.create_tag_display(tagList=list(self.tagsInImages))
        self.on_cancel_tags_button(Button())

    def create_addTag_img_button(self):
        """Create 'Add Tag' button for selected images.
        Creates a button labeled 'T+' to add a tag to the selected images. When clicked, it opens
        a popup where the user can enter a new tag. The tag is then added to the selected images.
        """
        self.add_tag_img_button = Button(text='T+', font_size=20, background_color='#94FFDA')
        self.add_tag_img_button.bind(on_press=lambda _, image=SelectableImage.selected_images: self.add_tag_img_popup(image))
        return self.add_tag_img_button

    def rem_remTagButton(self):
        """Remove the 'Remove Tag' button from the button bar.
        Removes the 'Remove Tag' button from the button bar if it is currently present.
        """
        if self.rem_tag_button in self.button_bar.children:
            self.button_bar.remove_widget(self.rem_tag_button)

    def rem_zipButton(self):
        """Remove the 'Zip' button from the button bar.
        Removes the 'Zip' button from the button bar if it is present.
        """
        if self.zip_button in self.button_bar.children:
            self.button_bar.remove_widget(self.zip_button)

    def rem_rotateButton(self):
        """Remove the 'Rotate' button from the button bar.
        Removes the 'Rotate' button from the button bar if it is present.
        """
        if self.rotate_button in self.button_bar.children:
            self.button_bar.remove_widget(self.rotate_button)


    def add_tag_img_popup(self, images):
        """Open a popup to add a tag to the selected images.
        Opens a popup window that allows the user to enter a tag name and add it to the selected images.
        """
        popup_content = BoxLayout(orientation='vertical', padding=10)
        tag_name = TextInput(multiline=False, hint_text='Enter Tag Name')
        addTag_button = Button(text='Add Tag')
        addTag_button.bind(on_press=lambda *args: self.add_tag_img(images=SelectableImage.selected_images, tag=tag_name.text, popup=popup))
        remPopup_button = Button(text="<")
        remPopup_button.bind(on_press=lambda *args: popup.dismiss())
        popup_content.add_widget(tag_name)
        popup_content.add_widget(addTag_button)
        popup_content.add_widget(remPopup_button)

        popup = Popup(title='Enter the new tag name', content=popup_content, size_hint=(0.4, 0.4))

        popup.open()

    def add_tag_img(self, images, tag, popup):
        """Add a tag to the selected images.
        Adds a specified tag to each of the selected images.
        """
        if tag not in self.addedTags and tag !="":
            self.addedTags.append(tag)
        for key in images.keys():
            selectableImg = images[key]
            selectableImg.add_tag(tag)
            self.tagsInImages.discard(tag)

            if self.tag_display in self.main_panel.children:
                self.main_panel.remove_widget(self.tag_display)
        popup.dismiss()

    def rotate_image(self, image=SelectableImage.selected_images):
        """Rotate the selected image by 90 degrees counter-clockwise.
        Rotates the selected image by 90 degrees counter-clockwise and saves the rotated image.
        """
        imageId = list(image.values())[0].id
        img_path = list(image.values())[0].image_source
        print("img_path = "+str(img_path))
        original_image = PILImage.open(img_path)
        rotated_img = original_image.rotate(-90, expand=True)
        width, height = original_image.size

        rotated_img.resize((height, width))
        rotated_img.save(img_path)
        self.images[imageId-1] = img_path
        SelectableImage.selected_images[imageId] = SelectableImage(img_path, id=imageId)
        SelectableImage.selected_images[imageId].image.reload()

        self.update_image_display()

    def zip_files_popup(self, images):
        """Open a popup to get the zip path and folder path for zipping the selected images.
        Opens a popup with text inputs for entering the zip path and folder path. It then calls the `zip_files` method with the selected images and the entered zip path and folder path.
        """
        # Create a popup with a text input for adding tags
        popup_content = BoxLayout(orientation='vertical', padding=10)
        zip_filename = TextInput(multiline=False, hint_text='Enter Zip Name')
        zip_folder = TextInput(multiline=False, hint_text='Enter full folderPath \n(write "default" for default)', text='')
        zip_button = Button(text='Ok')
        zip_button.bind(on_press=lambda *args: self.zip_files(images=SelectableImage.selected_images, zip_filename=zip_filename.text, zip_folder=zip_folder.text, popup=popup))
        popup_content.add_widget(zip_filename)
        popup_content.add_widget(zip_folder)
        popup_content.add_widget(zip_button)

        popup = Popup(title='Enter the zip path', content=popup_content, size_hint=(0.4, 0.4))

        popup.open()

    def zip_files(self, images, zip_filename, zip_folder, popup):
        """Zip the selected images into a .zip file.
        Takes the selected images, zip filename, zip folder, and a popup object.
        It creates a .zip file at the specified zip path and adds the selected images to it.
        """
        # Updated zip_files function using adjusted path separator
        if not zip_filename.endswith('.zip'):
            zip_filename += '.zip'

        if zip_folder == 'default':
            zip_folder = os.getcwd()

        zip_path = os.path.join(zip_folder, "ZippedImageFolder", zip_filename)
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

        with ZipFile(zip_path, 'w') as zip_object:
            # Adding files that need to be zipped
            for imageKey, image in images.items():
                image_source = image.image_source

                arcname = os.path.basename(image_source.replace("/", os.path.sep))

                zip_object.write(image_source, arcname=arcname)

        popup.dismiss()

    def setNewDate(self, btn):
        """Set a new date for the selected image.
        Allows the user to set a new date for the selected image. It opens a popup window with text inputs for entering the new day, month, and year. 
        After entering the values, the user can confirm the new date with the "Confirm" button.
        """
        last_key = list(SelectableImage.selected_images.keys())[-1]
        image = SelectableImage.selected_images[last_key]
        content = BoxLayout(orientation='horizontal')
        popup = Popup(title='Enter new Date (DD-MM-YYYY)', content=content, size_hint=(0.5, 0.2))

        newday = TextInput(multiline=False, hint_text="Insert day")
        newmonth = TextInput(multiline=False, hint_text="Insert month")
        newyear = TextInput(multiline=False, hint_text="Insert year")        
        content.add_widget(newday)
        content.add_widget(newmonth)
        content.add_widget(newyear)
        confirm_button = Button(text="Confirm")
        # date = str(newyear.text)+str(newmonth.text)+str(newday.text)+"00"+"00"+"00"
        confirm_button.bind(on_press=lambda *args: self.setDate(SelectableImage.selected_images, newyear.text, newmonth.text, newday.text, popup))
        content.add_widget(confirm_button)
        popup.open()

    def setDate(self, images, year, month, day, popup):
        """Set the date for the selected images.
        Sets the date for the selected images to the specified year, month, and day.
        The date is formatted as "YYYY:MM:DD 00:00:00". 
        If the input values for year, month, or day are not valid, an error message popup will be displayed.
        """
        if len(day) == 1:
            day = "0" + day
        if len(day) == 0:
            day = "00"
        if len(month) == 1:
            month = "0" + month
        if len(month) == 0:
            month = "00"

        try:
            datetime.datetime(year=int(year), month=int(month), day=int(day))
        except ValueError:
            # Invalid date input, display error message
            error_popup = Popup(title='Invalid Date', content=Label(text='Please enter a valid date.'), size_hint=(0.6, 0.4))
            error_popup.open()
            return

        date = year + ":" + month + ":" + day + " " + "00" + ":00" + ":00"
        for key in images.keys():
            selectableImg = images[key]
            selectableImg.set_date(date)
            popup.dismiss()
        self.update_image_display()
        self.dateLabel.text = "Date:" + date[:10]

    def create_date_label(self):
        """Create a button for displaying the date of the selected image(s).
        Creates a button widget that displays the date of the selected image(s).
        If only one image is selected, the button text will be in the format "Date: YYYY-MM-DD",
        where YYYY-MM-DD represents the date of the selected image.
        If no image is selected or multiple images are selected, the button text will be "Date:".
        Clicking on the button will open a popup window for setting a new date in the input format DD-MM-YYYY.
        """
        image = None
        for key in SelectableImage.selected_images:
            image = SelectableImage.selected_images[key]
        print("len(SelectableImage.selected_images) == 1")
        if image is not None:
            if len(SelectableImage.selected_images) == 1:
                self.dateLabel = Button(text="Date:"+image.cpimage.getDate()[:10], font_size=15,size_hint=(0.15,0.99), on_press=self.setNewDate, background_color='#94FFDA')
            else:
                self.dateLabel = Button(text="Date:", font_size=15,size_hint=(0.15,0.99), background_color='#94FFDA')
        else:
            self.dateLabel = Button(text="Date:", font_size=15,size_hint=(0.15,0.99), background_color='#94FFDA')

        return self.dateLabel

    def ok_button(self):
        """Create an OK button.
        Creates a button with the label "OK" that is used as a confirmation button.
        The button has a specified font size and background color. 
        It is bound to the `load_scene_w_tags1` method to trigger an action when pressed.
        """
        self.okButton = Button(text="OK", font_size=20, background_color="#94FFDA")
        self.okButton.bind(on_press=self.load_scene_w_tags1)
        return self.okButton        

    def load_tags(self, instance):
        """Load tags.
        Is triggered when the user selects the "T" button to load tags. It clears the main panel and button bar, and creates the necessary buttons and layouts to display and manage tags.
        """
        self.main_panel.clear_widgets()
        self.button_bar.clear_widgets()

        self.okButton = self.ok_button()
        self.button_bar.add_widget(self.okButton)

        self.reset_active_tags_button = Button(text='Reset', font_size=20, background_color="#94FFDA")
        self.reset_active_tags_button.bind(on_press=lambda *args: setattr(self, 'activeTags', []))

        self.addTags_to_main_button = Button(text="<", font_size=20, background_color="#94FFDA")
        self.addTags_to_main_button.bind(on_press=self.on_cancel_tags_button)
        self.button_bar.add_widget(self.addTags_to_main_button)
        self.button_bar.add_widget(self.reset_active_tags_button)

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
        """Add active tag.
        Is triggered when a tag button is pressed in the tag display.
        It adds the selected tag to the list of active tags.
        """
        if tag not in self.activeTags:
            print("add_activeTag tag = "+tag)
            self.activeTags.append(tag)

    def load_scene_w_tags1(self, instance):
        """Load scene with tags.
        Is triggered when the "OK" button is pressed after selecting tags.
         It loads the scene based on the selected tags, filters the images, and updates the image display.
        """
        SelectableImage.selected_images = {}
        self.main_panel.clear_widgets()
        self.button_bar.clear_widgets()
        self.button_bar = self.create_button_bar()
        self.main_panel.add_widget(self.button_bar)

        if self.reset_active_tags_button in self.button_bar.children:
            self.button_bar.remove_widget(self.reset_active_tags_button)
        self.main_panel.remove_widget(self.tag_display)
        self.main_panel.add_widget(self.image_display)

        self.addedTags = copy.deepcopy(self.activeTags)
        self.images = self.load_images_from_folder(self.image_folder)
        self.get_image_names(self.image_folder)
        
        print("self.image_folder = "+str(self.image_folder))
        imagesWithTags = list()
        image_names = []
        image_dirs = []
        if len(self.activeTags) >= 1:
            for image in self.images:
                image = image.replace("\\", "/")
                image = image.replace("//", "/")
                name = image.split("/")[-1]
                dir = "/".join(image.split("/")[:-1]) + "/"
                dir = dir.replace("\\", "/")
                dir = dir.replace("//", "/")
                print("image = " +str(image))
                print("dir = " +str(dir))
                print("name = " +str(name))
                image_dirs.append(dir)
                cpimage = CPImage(name, dir)
                for tag in self.activeTags:
                    if cpimage.hasTag(tag):
                        imagesWithTags.append(dir+"/"+name)
                        break
        else:
            for image in self.images:

                image = image.replace("\\", "/")
                image = image.replace("//", "/")
                name = image.split("/")[-1]
                dir = "/".join(image.split("/")[:-1]) + "/"
                dir = dir.replace("\\", "/")
                dir = dir.replace("//", "/")
                imagesWithTags.append(dir+"/"+name)
        self.images = imagesWithTags
        if len(self.activeTags) <=0:
            self.images = copy.deepcopy(self.original_images)
        print("Self.images= "+str(self.images))
        
        self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
        self.page_number=1
        self.update_image_display()
        self.bottom_row.clear_widgets()
        if self.bottom_row_label not in self.bottom_row.children:
            self.bottom_row.add_widget(self.bottom_row_label)
        self.add_pageIndex_prev_next_to_bottomRow()

    def create_search_button(self):
        """Create search button.
        Creates and returns a search button widget.
        """
        self.search_button = Button(text='S', font_size=20, background_color='#94FFDA')
        self.search_button.bind(on_press=self.load_tags)
        return self.search_button

    def load_images_from_folder(self, folder_path):
        """Load images from a folder.
        Loads and returns a list of image file paths from the specified folder path.
        It also updates the `addedTags` list with any tags found in the images.
        """
        self.images = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                fullPath = os.path.join(root, filename)
                if filename.endswith('.png') or filename.endswith('.jpg') and fullPath not in self.images:
                    self.images.append(fullPath)
                    imgTags = CPImage(imageFile=filename, dirPath=root).getTagsList()
                    for tag in imgTags:
                        if tag not in self.addedTags:
                            self.addedTags.append(tag)
        return self.images   
    
    def get_image_names(self, folder_path): #Name of image file
        """Get the names of image files in a folder.
        Recursively traverses the specified folder path and retrieves
        the names of all image files (ending with .png or .jpg) found within the folder and its sub folders.
        """
        for filename in os.listdir(folder_path):
            fullPath = os.path.join(folder_path, filename)
            if filename.endswith('.png') or filename.endswith('.jpg'):
                self.imageNames.append(filename)
            elif os.path.isdir(fullPath):
                self.get_image_names(fullPath)
        return self.imageNames

    def update_image_display(self, shuffle=False): 
        """Update the image display with the images to be shown on the current page.
        Clears the existing widgets in the image display and populates it
        with the images to be displayed on the current page.
        The images are selected based on the current page number and the number of images per page.
        """
        #Shuffle is false in all except first time 
        self.image_display.clear_widgets()

        start_index = (self.page_number - 1) * self.images_per_page
        end_index = self.page_number * self.images_per_page
        if shuffle == True: random.shuffle(self.images)
        images_to_display = self.images[start_index:end_index]

        if self.images_per_page >= 1 and self.images_per_page <= 3:
            max_images_per_row = 3
            max_rows = 1
        elif self.images_per_page == 4:
            max_images_per_row = 2
            max_rows = 2
        elif self.images_per_page ==5:
            max_images_per_row = 3
            max_rows = 2
        elif self.images_per_page >= 6 and self.images_per_page <= 12:
            max_images_per_row = 3
            max_rows = 4
        elif self.images_per_page >= 13 and self.images_per_page <= 20:
            max_images_per_row = 5
            max_rows = 4
        else:
            max_images_per_row = 5
            max_rows = 5

        images_count = len(images_to_display)
        rows = images_count // max_images_per_row
        if images_count % max_images_per_row != 0:
            rows += 1
        rows = min(rows, max_rows)

        image_index = start_index

        for i in range(rows):
            row_images = images_to_display[i * max_images_per_row:(i + 1) * max_images_per_row]
            row_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
            for image_path in row_images:
                image_index += 1

                image = SelectableImage(image_source=image_path, id=image_index)
                image.bind(on_release=self.on_image_selected)
                row_layout.add_widget(image)

            self.image_display.add_widget(row_layout)
            self.page_label.text = f'Page {self.page_number}'

    def on_image_selected(self, instance):
        """
        Perform actions when an image is selected.
        """
        print(f"Selected image: {instance.image_source}")
        
    def go_to_previous_page(self, instance):
        """
        Go to the previous page of images.
        """
        if self.page_number > 1:
            self.page_number -= 1
            self.update_image_display()

    def go_to_next_page(self, instance):
        """
        Go to the next page of images.
        """
        if self.page_number < self.total_pages:
            self.page_number += 1
            self.update_image_display()

    def get_cancel_button(self):
        """
        Get the cancel button assigned.
        """
        self.cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')
        self.cancel_button.bind(on_press=self.on_cancel_tags_button)
        return self.cancel_button

    def on_add_tags_button(self, instance):
        """Callback function when the add tags button is pressed.
        Removes the existing buttons from the button bar, creates and adds the save and cancel buttons,
        and updates the main panel layout to display the tag display.
        """
        # Remove the existing buttons from the button bar
        self.button_bar.clear_widgets()

        save_button = Button(text='+T', font_size=20, background_color='#94FFDA')
        cancel_button = Button(text='<', font_size=20, background_color='#94FFDA')

        save_button.bind(on_press=self.on_save_tags_button)
        cancel_button.bind(on_press=self.on_cancel_tags_button)

        self.button_bar.add_widget(save_button)
        self.button_bar.add_widget(cancel_button)

        self.main_panel.remove_widget(self.image_display)
        allTagsInImgs = list(self.addedTags)

        self.tag_display = self.create_tag_display(allTagsInImgs)
        if self.tag_display not in self.main_panel.children:
            self.main_panel.add_widget(self.tag_display)

    def create_tag_display(self, tagList):
        """Creates and returns a layout for displaying tags.
        The tags are arranged in multiple columns based on the given tag list.
        """
        print("ctd taglist = " + str(tagList) )
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
                        if tagList[x * colN + i1] == "": continue
                        b = Button(text=tagList[x * colN + i1], font_size=20, background_color="#94FFDA", size_hint=(0.3, 0.3))
                        tag_display1.add_widget(b)
                        print("tag_display1 adds = "+str(tagList[x * colN + i1]))
                    print("x * colN + i1 = "+str(x * colN + i1))
                self.tag_display.add_widget(tag_display1)
                print("tag_display "+ str(self.tag_display))

        return self.tag_display

    def on_save_tags_button(self, instance):
        """Performs actions when the "Save" button for tags is pressed.
        Displays a popup with a text input for adding tags.
        When the "Add" button in the popup is pressed, the entered tags are added using the add_tags method.
        The existing buttons in the button bar are cleared and new buttons are created and added.
        """
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
        """Performs actions when the "Delete" button for tags is pressed.
        Displays a popup with a text input for removing tags.
        When the "Delete" button in the popup is pressed, the entered tags are removed using the del_tag method.
        The existing buttons in the button bar are cleared and new buttons are created and added.
        """
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
        """Removes a tag from the list of added tags.
        Removes the specified tag from the list of added tags. If the tag does not exist
        in the list, no action is taken.
        """
        if tag not in self.addedTags:
            return
        self.addedTags.remove(tag)
        print(f"Tags: {tag}")
        print(self.addedTags)
        popup.dismiss()        

    def on_cancel_tags_button(self, instance):
        """Performs actions when the "Cancel" button is pressed in the tag display.
        Removes the tag display from the main panel and restores the original button bar layout.
        It also updates the selected images label and adds the image display back to the main panel.
        """
        if self.reset_active_tags_button in self.button_bar.children:
            self.button_bar.remove_widget(self.reset_active_tags_button)

        if self.tag_display in self.main_panel.children:
            self.main_panel.remove_widget(self.tag_display)
        search_button = self.create_search_button()
        self.button_bar.size_hint = (0.1, 1)
        self.button_bar.clear_widgets()
        self.button_bar.add_widget(self.collection_tags_button)
        self.button_bar.add_widget(search_button)
        self.update_selected_images_label()
        if self.image_display not in self.main_panel.children:
            self.main_panel.add_widget(self.image_display)
        if self.tag_display in self.main_panel.children:
            self.main_panel.remove_widget(self.tag_display)
        

    def add_tags(self, tags, popup):
        """Adds tags to the selected images.
        Adds the specified tags to the list of added tags and updates the tag display and bottom row label.
        It also dismisses the popup window.
        """
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

        # Update the bottom row label with the tags
        tag_text = "Tags: " + ", ".join(self.addedTags)
        self.bottom_row_label.text = tag_text

        popup.dismiss()

    def on_request_close(self, btn):
        """Handles the request to close the application.
        Displays a popup window asking if the collection should be saved before closing.
        The user can choose to save the collection or discard the changes.
        """
        content = BoxLayout(orientation = 'horizontal', spacing = '5')
        popup = Popup(title='Save Collection before leaving?', content = content, size_hint=(None, None), size=(600, 300))
        btn2 = Button(text='Yes', size_hint=(1, 0.25), on_release = self.saveImgCol)
        btn1 = Button(text='No', size_hint=(1, 0.25), on_release = self.stop)
        
        content.add_widget(btn2)
        content.add_widget(btn1)

        popup.open()
        return True
    
    def saveImgCol(self, btn):
        """
        Saves the collection in a file
        """
        images = self.images
        cpimgs = []
        for imagePath in images:
            foldername = "/".join(imagePath.split('/')[:-1]) 
            filename = imagePath.split('/')[-1]
            cpimage = CPImage(filename, foldername)
            cpimgs.append(cpimage)

        # dir = default_folder+"/imageCollections/"
        dir = os.getcwd()+"/imageCollections/"
        if not os.path.isdir(dir):
            os.makedirs(dir)
        imgCol = ImageCollection("imageCollection1.txt", [], dir)
        
        for cpimage in cpimgs:
            imgCol.registerItem(cpimage)
        imgCol.saveCollection()
        self.stop()

    def loadCol1(self, collection):
        """Loads an image collection from a file.
        Reads the image collection data from a file and populates the application
        with the images and tags from the collection.
        """
        try:
            files = []
            dir = default_folder + "/imageCollections/"
            dir = os.getcwd() + "/imageCollections/"
            if not os.path.isdir(dir):
                os.makedirs(dir)
            s = ""
            if not os.path.isfile(dir + "imageCollection1.txt"):
                raise FileNotFoundError("The image collection file was not found")

            with open(dir + "imageCollection1.txt", "r") as outfile:
                s = outfile.read()

            data = json.loads(s)
            print("JSON.LOADSSSSSSSSSSSSS =", data)

            filename = data["filename"]
            items = data["items"]

            print("ImageCollection filename:", filename)
            print("Number Of Items", len(items))

            imagePaths = []
            for item in items:
                image = item["Image"][0]
                folder = item["Folder"][0]
                imagePaths.append(folder + image)
                print("imagePath =", str(folder + image))
                if item["tags"] != []:
                    tags = item["tags"][0]
                else:
                    tags = []
                print("Image:", image)
                print("Folder:", folder)
                print("Tags:", tags)
            self.images = imagePaths
            if self.loadColButton in self.bottom_row.children:
                self.bottom_row.remove_widget(self.loadColButton)

            self.total_pages = (len(self.images)+self.images_per_page-1) // self.images_per_page
            self.page_number = 1
            self.update_image_display()

        except FileNotFoundError as e:
            # Show the error message in a popup
            error_message = str(e)
            popup = Popup(title="Error", content=Label(text=error_message), size_hint=(None, None), size=(400, 200))
            popup.open()
            
            # Clear the previous collection and update the image display
            self.images = []
            self.update_image_display()

    def open_folder_selection_popup(self, instance):
        """Opens a folder selection popup and loads images from the selected folder.
        Opens a popup window for selecting a folder on the system. Once a folder
        is selected, the method loads and displays the images from that folder in the application.
        The method also initializes the necessary variables for image handling.
        """
        default_folder = os.getcwd()

        folder_popup = FolderSelectionPopup(default_folder)
        folder_popup.select_folder()

        selected_folder = folder_popup.get_selected_folder()
        if selected_folder is not None:  # Check if a folder is selected
            default_folder = selected_folder
            if not default_folder.endswith("/"):
                default_folder += "/"
            print("Selected folder:", default_folder)
            # Load and display images from folder
            self.image_folder = default_folder
            if not os.path.isdir(self.image_folder):
                os.mkdir(self.image_folder)
            self.addedTags = []
            self.images = self.load_images_from_folder(self.image_folder)
            self.original_images = self.load_images_from_folder(self.image_folder)  # Backup images
            self.total_pages = (len(self.images) + self.images_per_page - 1) // self.images_per_page
            self.update_image_display(shuffle=True)

            # Remove the "Load previous collection" button from the button bar
            self.bottom_row.remove_widget(self.loadColButton)
        else:
            print("No folder selected")
            # Clear the image display
            self.image_folder = ""
            self.images = []
            self.original_images = []
            self.total_pages = 0
            self.update_image_display(shuffle=True)



PicLib().run()