from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal vertical com espaçamento e padding baseados na altura da janela (responsivo)
        layout = BoxLayout(
            orientation='vertical',
            spacing=Window.height * 0.03,  # Espaço entre widgets proporcional à altura da janela
            padding=Window.height * 0.05   # Espaço interno das bordas proporcional à altura da janela
        )

        layout.add_widget(Widget(size_hint=(1, 0.3)))  # Espaço vazio no topo para balancear visualmente

        # Label título com tamanho de fonte responsivo
        title = Label(
            text="Jogo da Memória",
            font_size=Window.height * 0.05,  # Fonte baseada na altura da janela
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        # Atualiza a propriedade text_size para centralizar o texto corretamente
        title.bind(size=self.update_label_text_size)

        # Botão para iniciar o jogo, com tamanho e posicionamento responsivos
        start_btn = Button(
            text="Iniciar Jogo",
            background_normal='',
            background_color=(0.1, 0.5, 0.8, 1),  # azul meio forte
            color=(1, 1, 1, 1),  # texto branco
            font_size=Window.height * 0.035,  # Fonte proporcional à altura da janela
            size_hint=(0.5, 0.15),             # Ocupa 70% da largura, 15% da altura do layout pai
            pos_hint={'center_x': 0.5}         # Centraliza horizontalmente
        )
        start_btn.bind(on_release=self.start_game)  # Evento que inicia o jogo

        # Adiciona widgets ao layout principal
        layout.add_widget(title)
        layout.add_widget(start_btn)
        layout.add_widget(Widget(size_hint=(1, 0.5)))  # Espaço vazio na parte inferior

        # Adiciona o layout completo à tela
        self.add_widget(layout)

    def update_label_text_size(self, instance, size):
        # Método para atualizar o tamanho do texto dentro da label para manter centralização
        instance.text_size = size

    def start_game(self, *args):
        # Método que troca para a tela do jogo ao clicar no botão
        self.manager.current = 'memory_game'
