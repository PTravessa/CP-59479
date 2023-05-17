class CentralPanel(BoxLayout):
    def __init__(self, app_layout, **kwargs):
        self.configPanel = ConfigPanel(app_layout)
        self.task1Panel = Task1Panel(app_layout)
        self.task2Panel = Task2Panel(app_layout)
        self.app_layout = app_layout
        self.add_widget(self.task1Panel)

    def showConfigPanel(self):
        self.clear_widgets()
        self.add_widget(self.configPanel)

    def showTask1Panel(self):
        self.clear_widgets()
        self.add_widget(self.task1Panel)

    def showTask2Panel(self):
        self.clear_widgets()
        self.add_widget(self.task2Panel)


class Task1Panel(BoxLayout):
    def __init__(self, app_layout, **kwargs):
        self.app_layout = app_layout
        # Other initialization code

    def findItems(self):
        items = # ...
        self.app_layout.bottomRow.displayNumItems(len(items))


class BottomRow(BoxLayout):
    def __init__(self, app_layout, **kwargs):
        self.app_layout = app_layout
        # Other initialization code

    def displayNumItems(self, n):
        self.label2.text = 'Num of items: ' + str(n)


class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.topRow = TopRow(self)
        self.mainPanel = MainPanel(self)
        self.bottomRow = BottomRow(self)
        super().__init__(**kwargs)

    def changeButtonBarPosition(self):
        # Method to change the position of the button bar
        pass


class MyApp(App):
    def build(self):
        return MyAppLayout()


if __name__ == '__main__':
    MyApp().run()
