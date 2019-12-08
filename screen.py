import pygame
import game


class Screen:

    def __init__(self):
        self.interface = None
        self.game = None
        self.screen = None
        self.font = None
        self.is_need_to_restart = False
        self.engine = game.GameEngine(self)
        self.mouse = (None, (0, 0, 0) )

    def init(self):
        pygame.display.init()
        if self.engine.settings.graphic['screen']['fullscreen']:
            self.screen = pygame.display.set_mode((self.engine.settings.graphic['screen']['resolution_x'],
                                                   self.engine.settings.graphic['screen']['resolution_y']),
                                                  pygame.FULLSCREEN | pygame.HWSURFACE, 32)
        else:
            self.screen = pygame.display.set_mode((self.engine.settings.graphic['screen']['resolution_x'],
                                                   self.engine.settings.graphic['screen']['resolution_y']))

        self.engine.settings.graphic['screen']['resolution_scale'] = (self.engine.settings.graphic['screen']['resolution_x']/1920,
                                                                      self.engine.settings.graphic['screen']['resolution_y']/1080)
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.font = pygame.font.Font(None, self.engine.settings.graphic['screen']['font_size'])
        pygame.display.set_caption(self.engine.settings.graphic['screen']['caption'])

    def change_resolution(self):
        self.is_need_to_restart = True

    def change_font_size(self):
        self.font = pygame.font.Font(None, screen.engine.settings.graphic['screen']['font_size'])

    def change_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def run(self):
        from data.modules.game_drawer import GameDrawer
        self.game = GameDrawer(self.engine, self)
        self.game.init()
        clock = pygame.time.Clock()
        all_ticks = 0
        while True:
            all_ticks += clock.tick(60)
            self.screen.fill( (0, 0, 0) )
            if self.is_need_to_restart:
                return True
            if self.interface is not None:
                self.interface.run()
            elif self.game is not None:
                self.mouse = (pygame.mouse.get_pos(), (0, 0, 0))
                self.game.mouse = self.mouse
                self.game.run()


if __name__ == '__main__':
    while True:
        screen = Screen()
        screen.init()
        screen.engine.init_state('/save_1', screen)
        screen.run()
