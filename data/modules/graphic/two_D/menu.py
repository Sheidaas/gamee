from .button import Button
from .background import Background
import pygame


class Menu:

    def __init__(self):
        self.background = None
        self.images = {}
        self.buttons = {}

    def create_buttons(self, screen):
        self.buttons = {}

        start = (480, 700)
        size = (200, 50)


        self.buttons['resume'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['menu']['resume'],
                                        screen.font, self.exit, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen)


        self.buttons['resume'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['menu']['resume'],
                                        screen.font, self.exit, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen)

        start = (480, 775)

        self.buttons['settings'] = Button(start[0], start[1], size[0], size[1],
                                          screen.engine.database.language.texts['gui']['menu']['settings'], screen.font,
                                          self.go_to_settings, screen.screen, screen.engine.settings.graphic['screen'],
                                          screen)

        start = (480, 850)

        self.buttons['main_menu'] = Button(start[0], start[1], size[0], size[1],
                                           screen.engine.database.language.texts['gui']['menu']['main_menu'], screen.font,
                                           self.go_to_main_menu, screen.screen,
                                           screen.engine.settings.graphic['screen'], screen)

        start = (480, 925)

        self.buttons['exit'] = Button(start[0], start[1], size[0], size[1],
                                      screen.engine.database.language.texts['gui']['menu']['exit'], screen.font, exit, screen.screen,
                                      screen.engine.settings.graphic['screen'], 0)

        self.images['logo'] = (pygame.image.load(screen.engine.path + '/data/graphic/logo/game_logo.png'),
                               (480 * screen.engine.settings.graphic['screen']['resolution_scale'][0],
                                400 * screen.engine.settings.graphic['screen']['resolution_scale'][1]))

    def create_background(self, screen):
        x1 = 200
        y1 = 0
        x2 = 1520
        y2 = 1680
        self.background = Background(x1, y1, x2, y2, (255, 255, 255), screen)

    def create(self, screen):
        self.create_buttons(screen)
        self.create_background(screen)

    @staticmethod
    def go_to_main_menu(screen):
        screen.game.gui['menu'] = False
        screen.game.gui['main_menu'] = True


    @staticmethod
    def go_to_settings(screen):
        screen.game.gui['menu'] = False
        screen.game.gui['settings'] = True

    @staticmethod
    def exit(screen):
        screen.game.gui['menu'] = False
