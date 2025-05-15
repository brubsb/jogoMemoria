from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty
import random

# Configurações do tabuleiro
ROWS = 4  # Quantidade de linhas
COLS = 5  # Quantidade de colunas
TOTAL_CARDS = ROWS * COLS  # Total de cartas no tabuleiro

# Letras usadas para formar pares (10 pares no total)
letters = list('ABCDEFGHIJ')
cards = letters * 2  # Duas cartas para cada letra (pares)
random.shuffle(cards)  # Embaralha as cartas no início

def clamp(value, min_value, max_value):
    # Função para limitar um valor entre mínimo e máximo
    return max(min_value, min(value, max_value))

class MemoryGameScreen(Screen):
    # Propriedades que definem tamanhos responsivos baseados na janela
    header_height = NumericProperty(Window.height * 0.08)
    font_size_back_button = NumericProperty(clamp(Window.height * 0.035, 14, 24))  # Fonte do botão Voltar
    font_size_title = NumericProperty(clamp(Window.height * 0.045, 18, 32))       # (opcional) Fonte do título

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Atualiza tamanhos quando a janela é redimensionada
        Window.bind(on_resize=self.update_sizes)

        # Estado do jogo
        self.buttons = []             # Lista dos botões das cartas
        self.first_card = None        # Primeira carta virada
        self.second_card = None       # Segunda carta virada
        self.revealed = [False] * TOTAL_CARDS  # Cartas que já foram reveladas e combinadas
        self.locked = False           # Controle para evitar virar cartas enquanto checa pares

        # Layout principal vertical
        self.main_layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # Cabeçalho com botão Voltar
        self.header = BoxLayout(size_hint_y=None, height=self.header_height, padding=(5, 0), spacing=10)

        self.back_button = Button(
            text='← Voltar',
            font_size=self.font_size_back_button,
            size_hint=(None, 1),   # largura fixa, altura relativa ao pai
            width=100,
            halign='center',
            valign='middle',
            shorten=True,
            shorten_from='right'
        )
        self.back_button.bind(on_release=self.go_back)  # Voltar para tela inicial
        self.header.add_widget(self.back_button)

        # Grade das cartas do jogo
        self.grid = GridLayout(cols=COLS, rows=ROWS, spacing=5, padding=5)
        self.create_board()  # Cria os botões das cartas

        # Monta a tela
        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(self.grid)
        self.add_widget(self.main_layout)

    def update_sizes(self, instance, width, height):
        # Atualiza tamanhos responsivos ao redimensionar a janela
        self.header_height = height * 0.08
        self.font_size_back_button = clamp(height * 0.035, 14, 24)
        self.header.height = self.header_height
        self.back_button.font_size = self.font_size_back_button
        # Se usar título, atualize aqui também

    def go_back(self, *args):
        # Volta para a tela inicial
        self.manager.current = 'home'

    def create_board(self):
        # Cria o grid de botões das cartas
        self.buttons = []
        self.grid.clear_widgets()
        for i in range(ROWS):
            for j in range(COLS):
                idx = i * COLS + j
                btn = Button(text='?', font_size='32sp')  # Cartas inicialmente escondidas (?)
                btn.bind(on_release=lambda btn, i=i, j=j: self.on_card_click(i, j))  # Evento ao clicar na carta
                self.grid.add_widget(btn)
                self.buttons.append(btn)

    def on_card_click(self, i, j):
        # Lógica para virar as cartas
        if self.locked:
            return  # Se o jogo está "travado" aguardando verificação, ignore cliques

        idx = i * COLS + j
        if self.revealed[idx] or self.buttons[idx].text != '?':
            return  # Se carta já revelada ou já virada, ignore clique

        self.buttons[idx].text = cards[idx]  # Mostra a letra da carta clicada

        if not self.first_card:
            self.first_card = (i, j)  # Guarda a primeira carta virada
        elif not self.second_card and (i, j) != self.first_card:
            self.second_card = (i, j)  # Guarda a segunda carta
            self.locked = True          # Trava o jogo até checar se cartas combinam
            Clock.schedule_once(self.check_match, 1)  # Verifica após 1 segundo

    def check_match(self, dt):
        # Checa se as duas cartas são iguais
        i1, j1 = self.first_card
        i2, j2 = self.second_card
        idx1 = i1 * COLS + j1
        idx2 = i2 * COLS + j2

        if cards[idx1] == cards[idx2]:
            # Se combinam, marca como reveladas
            self.revealed[idx1] = True
            self.revealed[idx2] = True
        else:
            # Se não combinam, esconde as cartas novamente
            self.buttons[idx1].text = '?'
            self.buttons[idx2].text = '?'

        # Reseta seleção
        self.first_card = None
        self.second_card = None
        self.locked = False

        # Se todas as cartas foram reveladas, mostra mensagem de vitória
        if all(self.revealed):
            self.show_victory_message()

    def show_victory_message(self):
        # Limpa a tela e mostra mensagem de vitória com opções
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        label = Label(text="🎉 Você venceu!", font_size='32sp', size_hint=(1, 0.5))
        layout.add_widget(label)

        btn_play_again = Button(text="Jogar novamente", size_hint=(1, 0.25))
        btn_play_again.bind(on_release=self.restart_game)
        layout.add_widget(btn_play_again)

        btn_back_home = Button(text="Voltar para o menu", size_hint=(1, 0.25))
        btn_back_home.bind(on_release=self.go_back)
        layout.add_widget(btn_back_home)

        self.add_widget(layout)

    def restart_game(self, *args):
        # Reinicia o jogo: embaralha cartas, reseta estado e redesenha o tabuleiro
        global cards
        random.shuffle(cards)

        self.clear_widgets()
        self.revealed = [False] * TOTAL_CARDS
        self.first_card = None
        self.second_card = None
        self.locked = False

        self.main_layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        self.header = BoxLayout(size_hint_y=None, height=self.header_height, padding=(5, 0), spacing=10)
        self.back_button = Button(
            text='← Voltar',
            font_size=self.font_size_back_button,
            size_hint=(None, 1),
            width=100,
            halign='center',
            valign='middle',
            shorten=True,
            shorten_from='right'
        )
        self.back_button.bind(on_release=self.go_back)
        self.header.add_widget(self.back_button)

        self.grid = GridLayout(cols=COLS, rows=ROWS, spacing=5, padding=5)
        self.create_board()

        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(self.grid)
        self.add_widget(self.main_layout)
