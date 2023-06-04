import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.size = (900, 600)

class Main(App):
    def build(self):
        main_box = BoxLayout(orientation='vertical', size_hint=(1, 1))
        button_box = BoxLayout(orientation='vertical', size_hint=(0.1, 0.9))
        
        self.buttonFillU = Button(text='', font_size=15, size_hint=(1, 0.1), height=40)
        self.buttonA = Button(text='A', font_size=15, size_hint=(1, None), height=40)
        self.buttonB = Button(text='B', font_size=15, size_hint=(1, None), height=40)
        self.buttonC = Button(text='C', font_size=15, size_hint=(1, None), height=40)
        self.buttonD = Button(text='D', font_size=15, size_hint=(1, None), height=40)
        self.buttonFillD = Button(text='', font_size=15, size_hint=(1, 0.1), height=40)
        button_box.add_widget(self.buttonFillU)
        button_box.add_widget(self.buttonA)
        button_box.add_widget(self.buttonB)
        button_box.add_widget(self.buttonC)
        button_box.add_widget(self.buttonD)
        button_box.add_widget(self.buttonFillD)
        self.label = Label(text=' It`s me! \n PicLib!!', font_size=50, color=(1, 0.5, 0.3, 1))
        self.buttonMainD = Button(text='bottom bar', font_size=15, size_hint=(1,0.1), height=40)

        
        main_box.add_widget(button_box)
        main_box.add_widget(self.label)
        main_box.add_widget(self.buttonMainD)
        
        return main_box

Main().run()
