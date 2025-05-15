from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from home_screen import HomeScreen
from memory_game_screen import MemoryGameScreen

class MemoryApp(App):
    def build(self):
        # Cria um gerenciador de telas (sem transição animada)
        sm = ScreenManager(transition=NoTransition())

        # Adiciona a tela inicial e a tela do jogo
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MemoryGameScreen(name='memory_game'))

        # Retorna o gerenciador de telas para ser exibido
        return sm

if __name__ == '__main__':
    MemoryApp().run()  # Executa o app
