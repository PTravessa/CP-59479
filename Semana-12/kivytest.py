import kivy
# Imports 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
#import os
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# A kivy application is made by sub-classing the App kivy class:
class FirstTest(App):
    
    # We must redefine (override) the build method:
    def build(self):
        # All widgets will be arranged in a BoxLayout:
        box = BoxLayout()
        self.label = Label(text='this is my first label', font_size=20)
        self.button1 = Button(text='button1', font_size=50)
        box.add_widget(self.label)
        box.add_widget(self.button1)
        self.button1.bind(on_press = self.doSomething)
        # we MUST return the main root widget:
        return box

    def doSomething(self,theButton):
        print('button1 was pressed.')

FirstTest().run()