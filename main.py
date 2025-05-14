from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from home_screen import HomeScreen
from memory_game_screen import MemoryGameScreen

class MemoryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MemoryGameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MemoryApp().run()
