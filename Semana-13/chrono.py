import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window

from datetime import datetime

Window.size = (900,600)

# A kivy application is made by sub-classing the App kivy class:
class Chrono(App):

    # We must redefine (override) the build method:
    def build(self):
        # the start attribute is used to display the elapsed time:
        self.start = datetime.now()
        # All widgets will be arranged in a vertical BoxLayout:
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # The row of buttons is also a BoxLayout:
        buttonRow = BoxLayout(orientation='horizontal', spacing=20, padding=15)
        # first row of saved times
        savedTimes1 = BoxLayout(orientation='horizontal', spacing=9, padding=12)
        # second row of saved times
        savedTimes2 = BoxLayout(orientation='horizontal', spacing=9, padding=12)
        # A label is used to display the time:
        self.label = Label(text=self.getTime(), font_size=100,
                           color=(231/255, 98/255, 203/255, 1))
        # A label to show the saved times 1
        self.label2 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 2
        self.label3 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 3
        self.label4 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 4
        self.label5 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 5
        self.label6 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 6
        self.label7 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 7
        self.label8 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 8
        self.label9 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 9
        self.label10 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # A label to show the saved times 10
        self.label11 = Label(text=" ", font_size=50,color=(0, 98/255, 203/255, 1))
        # The first button is for Start/Pause/Resume the chronograph
        self.button1 = Button(text='Start', font_size=50)
        # The second button is for resetting the chronograph
        self.button2 = Button(text='Reset', font_size=50)
        # The third button is for saving the time
        self.button3 = Button(text='Save', font_size=50)
        # Add widgets to layouts:
        box.add_widget(self.label)
        box.add_widget(savedTimes1)
        box.add_widget(savedTimes2)
        savedTimes1.add_widget(self.label2)
        savedTimes1.add_widget(self.label3)
        savedTimes1.add_widget(self.label4)
        savedTimes1.add_widget(self.label5)
        savedTimes1.add_widget(self.label6)
        savedTimes2.add_widget(self.label7)
        savedTimes2.add_widget(self.label8)
        savedTimes2.add_widget(self.label9)
        savedTimes2.add_widget(self.label10)
        box.add_widget(buttonRow)
        buttonRow.add_widget(self.button1)
        buttonRow.add_widget(self.button3)
        buttonRow.add_widget(self.button2)
        # Set the methods that will be called when buttons are pressed:
        self.button1.bind(on_press=self.startPausePressed)
        self.button2.bind(on_press=self.resetPressed)
        self.button3.bind(on_press=self.savePressed)
        # Define an attribute that will hold a periodic event for the
        # chronograph
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
        self.label.text = self.getTime()

        labels = [self.label2, self.label3, self.label4, self.label5, self.label6,
                self.label7, self.label8, self.label9, self.label10, self.label11]

        for label in labels:
            label.text = " "
            
    def startPausePressed(self, b):
        """
        startPausePressed is called when the Start/Pause/Resume
        button is pressed.
        The button text is used to select the action to be done.
        The button label is updated accordingly.
        """
        if self.button1.text == 'Start':
            self.start = datetime.now()
            self.chronoEvent = Clock.schedule_interval(self.setTimeValue,
                                                       1.0/2.0)
            self.button1.text = 'Pause'
        elif self.button1.text == 'Pause':
            self.clock = datetime.now()
            self.chronoEvent.cancel()
            self.button1.text = 'Resume'
        elif self.button1.text == 'Resume':
            self.start = datetime.now() - self.clock + self.start
            self.chronoEvent = Clock.schedule_interval(self.setTimeValue,
                                                       1.0/100)
            self.button1.text = 'Pause'
    def savePressed(self, b):
        labels = [self.label2, self.label3, self.label4, self.label5, self.label6,
                self.label7, self.label8, self.label9, self.label10, self.label11]

        for i in range(len(labels)):
            if labels[i].text == " ":
                labels[i].text = self.label.text
                break

    

Chrono().run()