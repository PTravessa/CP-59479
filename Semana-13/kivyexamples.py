import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from coloredlabel import ColoredLabel
from coloredboxlayout import ColoredBoxLayout


class Basic1(App):

    def build(self):
        box = BoxLayout()
        label1 = Label(text='this is a label.', font_size=50)
        label2 = ColoredLabel(text='this is a RED label.',
                              background_color=(1, 0, 0, 1), font_size=50)
        box.add_widget(label1)
        box.add_widget(label2)
        return box


# Basic1().run()

class Basic2(App):
    def build(self):
        box = ColoredBoxLayout(background_color=(149/255, 197/255, 246/255, 1)
                               )
        box.orientation = 'vertical'
        label1 = Label(text='this is a label. The background is transparent.', font_size=20)
        label2 = ColoredLabel(text='this is a RED label.',
                              background_color=(1, 0, 0, 1), font_size=40)
        # to specify the height of the label:
        label2.height = 100
        # to prevent kivy to recalculate the height: 
        label2.size_hint_y = None
        # to add space between the layout border and its elements.
        box.padding = (50, 50)
        box.add_widget(label1)
        box.add_widget(label2)
        return box
    
# Basic2().run()

class Basic3(App):
    def build(self):
        rootbox = ColoredBoxLayout(background_color=(149/255, 197/255, 246/255, 1))
        box = ColoredBoxLayout(background_color=(123/255, 211/255, 146/255, 1))
        box.orientation = 'vertical'
        
        label1 = Label(text='this is a label. The background is transparent.', font_size=10)
        label2 = ColoredLabel(text='this is a RED label.',
                              background_color=(1, 0, 0, 1), font_size=10)
        # to specify the height of the label:
        label2.height = 100
        # to prevent kivy to recalculate the height: 
        label2.size_hint_y = None
        # to add space between the layout border and its elements.
        box.padding = (50, 50)
        box.add_widget(label1)
        box.add_widget(label2)
        box.width = 250
        box.size_hint_x = None
        label3 = ColoredLabel(text='this is a girly label.',
                              background_color=(237/255, 178/255, 223/255, 1),
                              font_size=40)
        rootbox.add_widget(label3)
        rootbox.add_widget(box)
        return rootbox

Basic3().run()
