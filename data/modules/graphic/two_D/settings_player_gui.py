from .button import Button


class Settings:

    def __init__(self):
        self.images = {}
        self.background = None
        self.buttons = {}
        self.update = False

    def create_buttons(self, screen):
        self.buttons = {}
        start = (480, 420)

        size = (300, 50)

        self.buttons['resume'] = Button(start[0], start[1], size[0], size[1],
                                        screen.engine.database.language.texts['gui']['player_gui']['resume'], screen.font,
                                               self.exit, screen.screen, screen.engine.settings.graphic['screen'], screen)

        start = (480, 495)

        for key in screen.engine.database.language.texts['gui']['player_gui'].keys():
            if key != 'resume':
                text = screen.engine.database.language.texts['gui']['player_gui'][key] + str(screen.engine.settings.graphic['screen']['player'][key])
                self.buttons[key] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                                self.change_gui, screen.screen, screen.engine.settings.graphic['screen'], screen.engine.settings.graphic['screen'], key, screen)
                x, y = start[0], start[1]
                start = (x, y+75)

        self.update = False

    def change_gui(self, settings, key, screen):
        self.update = True
        if settings['player'][key]:
            settings['player'][key] = False
        else:
            settings['player'][key] = True
        screen.engine.save_settings()

    @staticmethod
    def exit(screen):
        screen.game.gui['settings'] = True
        screen.game.gui['settings_gui'] = False
        screen.game.drawer.gui['settings_gui'] = None