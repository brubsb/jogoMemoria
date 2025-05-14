from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

# Emojis: 18 pares para 6x6
emojis = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊',
          '🐻', '🐼', '🐨', '🐯', '🦁', '🐮',
          '🐷', '🐸', '🐵', '🐙', '🐔', '🦄']
cards = emojis * 2
random.shuffle(cards)

class MemoryGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.revealed = [False] * 36

        self.grid = GridLayout(cols=4, spacing=5, padding=10)
        self.create_board()
        self.add_widget(self.grid)

    def create_board(self):
        for i in range(8):
            for j in range(4):
                idx = i * 6 + j
                btn = Button(text='?', font_size='24sp')
                btn.bind(on_release=lambda btn, i=i, j=j: self.on_card_click(i, j))
                self.grid.add_widget(btn)
                self.buttons.append(btn)

    def on_card_click(self, i, j):
        idx = i * 6 + j
        if self.revealed[idx] or self.buttons[idx].text != '?':
            return

        self.buttons[idx].text = cards[idx]

        if not self.first_card:
            self.first_card = (i, j)
        elif not self.second_card and (i, j) != self.first_card:
            self.second_card = (i, j)
            Clock.schedule_once(self.check_match, 1)

    def check_match(self, dt):
        i1, j1 = self.first_card
        i2, j2 = self.second_card
        idx1 = i1 * 6 + j1
        idx2 = i2 * 6 + j2

        if cards[idx1] == cards[idx2]:
            self.revealed[idx1] = True
            self.revealed[idx2] = True
        else:
            self.buttons[idx1].text = '?'
            self.buttons[idx2].text = '?'

        self.first_card = None
        self.second_card = None

        if all(self.revealed):
            self.grid.clear_widgets()
            self.grid.add_widget(Label(text="🎉 Você venceu!", font_size='30sp'))
