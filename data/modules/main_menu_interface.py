from .graphic.interface_drawer import InterfaceDrawer
from .game_drawer import GameDrawer


class MainMenuInterface:

    def __init__(self, screen):
        self.screen = screen
        self.buttons = {
        'new_game': ['New Game', self],
        }

        drawer = InterfaceDrawer()

    def create(self):
        pass


    def draw(self):
        pass

    def run(self):
        self.get_event()
        self.draw()

    def get_event(self):
        pass

    def new_game(self):
        pass

    def load_game(self):
        pass
