import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class PicLib(App):
    def __init__(self, **kwargs):
        """
        Initialize the PicLib.

        Args:
            kwargs: Keyword arguments.

        Returns:
            None by Default
        """
        super().__init__(**kwargs)
        self.top_row = None  #BoxLayout
        self.bottom_row = None  #BoxLayout
        self.main_panel = None  #BoxLayout

    def build(self):
        """
        Builds the main interface.

        Returns:
            BoxLayout: The main layout of the app.
        """
        self.create_top_row()
        self.create_bottom_row()
        self.create_main_panel()

        # Main Layout
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.top_row)
        main_layout.add_widget(self.main_panel)
        main_layout.add_widget(self.bottom_row)

        return main_layout

    def create_top_row(self):
        """
        Creates the top row of the application.

        Returns:
            Nothing, Top filler panel.
        """
        self.top_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_row_label = Label(text='PicLib', font_size=40)
        self.top_row.add_widget(top_row_label)

    def create_bottom_row(self):
        """
        Creates the bottom row of the application.

        Returns:
            Nothing, Bottom filler panel.
        """
        self.bottom_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        bottom_row_label = Label(text='Main Page', font_size=30)
        self.bottom_row.add_widget(bottom_row_label)

    def create_main_panel(self):
        """
        Creates the main panel of the application.

        Returns:
            Nothing, Main filler panel.
        """
        self.main_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_bar = self.create_button_bar()
        image_display = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        self.main_panel.add_widget(button_bar)
        self.main_panel.add_widget(image_display)

    def create_button_bar(self):
        """
        Creates the button bar of the application.

        Returns:
            BoxLayout: The Left button bar layout.
        """
        button_bar = BoxLayout(orientation='vertical', size_hint=(0.1, 1))

        add_tags_button = Button(text='+T', font_size=20)
        remove_tags_button = Button(text='-T', font_size=20)
        search_button = Button(text='S', font_size=20)
        zip_button = Button(text='Zip', font_size=20)
        rotate_button = Button(text='R90', font_size=20)

        button_bar.add_widget(add_tags_button)
        button_bar.add_widget(remove_tags_button)
        button_bar.add_widget(search_button)
        button_bar.add_widget(zip_button)
        button_bar.add_widget(rotate_button)

        return button_bar

PicLib().run()

"""Temos o layout das 3 caixas necessárias,
os botões das tags estão definidos no entanto
acho que não temos o Save pretendido não sei se é o das tags ou não,
nós temos o do self.filename no ImageCollection,
falta-nos o Zip peço que confirmes sff e falta o Rotation90 degree,
em relação ao bidding das imagens para darem showcase
estava a pensar secalhar em grid?Para ficarem todas juntinhas
sem ocupar diferentes tamanhos no main ficava mais clean
no entanto não se dá para fazer como estou a pensar,
aos botões vou lhes meter colors type HEX, é mais universal
no entanto é irrelevante"""

"""Outra coisa, deves ter de instalar o sdl12 do kivy,
(pip install "kivy[sdl2]") no terminal """