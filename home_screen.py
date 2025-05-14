from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        layout.add_widget(Widget(size_hint=(1, 0.3)))  # Espaço superior

        title = Label(
            text="🧠 Jogo da Memória",
            font_size='32sp',
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))

        start_btn = Button(
            text="Iniciar Jogo",
            font_size='24sp',
            size_hint=(0.7, 0.15),
            pos_hint={'center_x': 0.5}
        )
        start_btn.bind(on_release=self.start_game)

        layout.add_widget(title)
        layout.add_widget(start_btn)
        layout.add_widget(Widget(size_hint=(1, 0.5)))  # Espaço inferior

        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'
