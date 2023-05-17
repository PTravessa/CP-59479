import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.size = (900,600)
class MainBoxLayout(App):
    def build(self):
        box = BoxLayout(orientation='vertical', padding=20, spacing=20)
        button1 = Button(text='Hi!', size_hint=(None, None), height=50)
        box.add_widget(button1, height=50)

        buttonRow = BoxLayout(orientation='horizontal', spacing=20, padding=15)
        button2 = Button(text='Button 1', size_hint=(None, None), height=50)
        buttonRow.add_widget(button2)

        
        box.add_widget(buttonRow)
        
        return box

# class MyApp(App):
#     def build(self):
#         return MainBoxLayout()


MainBoxLayout().run()        