import kivy

# Imports 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window

from datetime import datetime

Window.size = (600,360)

# A kivy application is made by sub-classing the App kivy class:
class Chrono(App):
    
    # We must redefine (override) the build method:
    def build(self):
        # the start attribute is used to display the elapsed time: 
        self.start = datetime.now()
        # All widgets will be arranged in a vertical BoxLayout:
        box = BoxLayout(orientation='vertical', padding=50, spacing=20)
        # The row of buttons is also a BoxLayout:
        buttonRow = BoxLayout(orientation='horizontal',spacing=20,padding=15)
        # A label is used to display the time:
        self.label = Label(text=self.getTime(), font_size=70, color=(1,1,1,1))
        # The first button is for Start/Pause/Resume the chronograph
        self.button1 = Button(text='Start', font_size=50)
        # The second button is for resetting the chronograph
        self.button2 = Button(text='Reset', font_size=50)
        # Add widgets to layouts:
        box.add_widget(self.label)
        buttonRow.add_widget(self.button1)
        buttonRow.add_widget(self.button2)
        box.add_widget(buttonRow)
        # Set the methods that will be called when buttons are pressed:
        self.button1.bind(on_press = self.startPausePressed)
        self.button2.bind(on_press = self.resetPressed)
        # Define an attribute that will hold a periodic event for the chronograph
        self.chronoEvent = None
        # the clock attribute is usefull for pause/resume operations
        self.clock = 0
        # we MUST return the main root widget:
        return box

    def getTime(self):
        """
        getTime: returns the elapsed time since start.

        Returns:
            [string]: a time amount following the format 'HH:MM:SS'
        """
        t = datetime.now() - self.start
        return str(t)[:-7]

    def setTimeValue(self, x):
        """
        setTimeValue Updates the label with elapsed time. This function 
        is called periodically.
        """
        self.label.text = self.getTime()
    

    def resetPressed(self, b):
        """
        resetPressed is called when the reset button is pressed.
        It resets the chronograph.
        """
        self.start = datetime.now()
        
    def startPausePressed(self, b):
        """
        startPausePressed is called when the Start/Pause/Resume 
        button is pressed.
        The button text is used to select the action to be done. 
        The button label is updated accordingly.
        """
        if self.button1.text == 'Start':
            self.start = datetime.now()
            self.chronoEvent = Clock.schedule_interval(self.setTimeValue, 1.0/2.0)
            self.button1.text = 'Pause'
        elif self.button1.text == 'Pause':
            self.clock = datetime.now()            
            self.chronoEvent.cancel()
            self.button1.text = 'Resume'
        elif self.button1.text == 'Resume':
            self.start = datetime.now() - self.clock + self.start 
            self.chronoEvent = Clock.schedule_interval(self.setTimeValue, 1.0/100)
            self.button1.text = 'Pause'

            

## testing

Chrono().run()


