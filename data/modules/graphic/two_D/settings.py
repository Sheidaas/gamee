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

        size = (200, 50)

        self.buttons['resume'] = Button(start[0], start[1], size[0], size[1],
                                        screen.engine.database.language.texts['gui']['settings']['resume'], screen.font,
                                               self.exit, screen.screen, screen.engine.settings.graphic['screen'], screen)

        start = (480, 495)

        text = screen.engine.database.language.texts['gui']['settings']['antialias'] + str(screen.engine.settings.graphic['screen']['antialias'])
        self.buttons['change_antialias'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          self.change_antialias, screen.screen, screen.engine.settings.graphic['screen'],
                                                  screen)

        start = (480, 570)

        text = screen.engine.database.language.texts['gui']['settings']['fullscreen'] + str(screen.engine.settings.graphic['screen']['fullscreen'])
        self.buttons['change_fullscreen'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          self.change_fullscreen, screen.screen, screen.engine.settings.graphic['screen'], screen)

        start = (405, 645)
        size = (50, 50)
        self.buttons['font_size_minus'] = Button(start[0], start[1], size[0], size[1], '-', screen.font,
                                          self.change_font_size, screen.screen, screen.engine.settings.graphic['screen'], screen, '-')

        start = (480, 645)
        size = (200, 50)
        text = screen.engine.database.language.texts['gui']['settings']['font_size'] + str(screen.engine.settings.graphic['screen']['font_size'])
        self.buttons['font_size'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          None, screen.screen, screen.engine.settings.graphic['screen'], 0)

        start = (705, 645)
        size = (50, 50)
        self.buttons['font_size_plus'] = Button(start[0], start[1], size[0], size[1], '+', screen.font,
                                          self.change_font_size, screen.screen, screen.engine.settings.graphic['screen'], screen, '+')

        start = (405, 720)
        size = (50, 50)
        self.buttons['resolution_minus'] = Button(start[0], start[1], size[0], size[1], '-', screen.font,
                                          self.change_resolution, screen.screen, screen.engine.settings.graphic['screen'], screen, '-')

        start = (480, 720)
        size = (200, 50)
        text = str(screen.engine.settings.graphic['screen']['resolution_x'])+ 'x' + str(screen.engine.settings.graphic['screen']['resolution_y'])
        self.buttons['resolution'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          None, screen.screen, screen.engine.settings.graphic['screen'], 0)

        start = (705, 720)
        size = (50, 50)
        self.buttons['resolution_plus'] = Button(start[0], start[1], size[0], size[1], '+', screen.font,
                                          self.change_resolution, screen.screen, screen.engine.settings.graphic['screen'], screen, '+')

        start = (480, 795)
        size = (200, 50)
        text = screen.engine.database.language.texts['gui']['settings']['change_gui']
        self.buttons['settings_gui'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          self.go_to_player_settings, screen.screen, screen.engine.settings.graphic['screen'], screen,)

        self.update = False

    def go_to_player_settings(self, screen):
        screen.game.gui['settings'] = False
        screen.game.gui['settings_gui'] = True


    def change_resolution(self, screen, char):
        self.update = True
        if char == '-':
            key = 1
            for resolution in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                if screen.engine.settings.graphic['screen']['resolution_x'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][0] and \
                        screen.engine.settings.graphic['screen']['resolution_y'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][1]:
                    key = int(resolution)
                    break
            if key == 1:
                for index in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                    if key < int(index):
                        key = int(index)
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]
            else:
                key -= 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]

        else:
            key = 1
            for resolution in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                if screen.engine.settings.graphic['screen']['resolution_x'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][0] and \
                    screen.engine.settings.graphic['screen']['resolution_y'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][1]:
                    key = int(resolution)
                    break
            if key == len(screen.engine.settings.graphic['screen']['avaible_resolutions']):
                key = 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]
            else:
                key += 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]

        screen.engine.save_settings()
        screen.change_resolution()

    def change_font_size(self, screen, char):
        self.update = True
        if char == '-':
            if screen.engine.settings.graphic['screen']['font_size'] > 18:
                screen.engine.settings.graphic['screen']['font_size'] -= 1
        else:
            if screen.engine.settings.graphic['screen']['font_size'] < 30:
                screen.engine.settings.graphic['screen']['font_size'] += 1
        screen.change_font_size()
        screen.engine.save_settings()

    def change_fullscreen(self, screen):
        self.update = True
        if screen.engine.settings.graphic['screen']['fullscreen']:
            screen.engine.settings.graphic['screen']['fullscreen'] = False
            screen.change_fullscreen()
        else:
            screen.engine.settings.graphic['screen']['fullscreen'] = True
            screen.change_fullscreen()
        screen.engine.save_settings()

    def change_antialias(self, screen):
        self.update = True
        if screen.engine.settings.graphic['screen']['antialias'] == 0:
            screen.engine.settings.graphic['screen']['antialias'] = 1
        else:
            screen.engine.settings.graphic['screen']['antialias'] = 0
        screen.engine.save_settings()

    @staticmethod
    def exit(screen):
        screen.game.gui['settings'] = False
        screen.game.gui['menu'] = True