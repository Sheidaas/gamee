import pygame
from .gui_abstract_object import GuiAbstractObject


class Health(GuiAbstractObject):

    def __init__(self, x, y, player, screen):
        super().__init__()
        self.player = player
        self.position = (x, y, 400, 40)
        self.rects_pos = {
            'main': ((), ()),
            'black_hp': ((), ()),
            'hp': ((), ()),
        }
        self.string = {
            'hp': (None, ())
        }
        self.screen = screen

    def create(self):
        position = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    self.position[2] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[3] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])

        self.rects_pos['main'] = (position, (255, 255, 255))
        pygame.draw.rect(self.screen.screen, self.rects_pos['main'][1], self.rects_pos['main'][0])
        position = ((self.position[0] + 10) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    (self.position[1] + 10) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    380 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    20 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])

        self.rects_pos['black_hp'] = (position, (0, 0, 0))
        pygame.draw.rect(self.screen.screen, self.rects_pos['black_hp'][1], self.rects_pos['black_hp'][0])

        text = str(self.player.statistics.health_points) + '/' + str(self.player.statistics.max_health_points)

        self.string['hp'] = (text, position)
        health_percent = (self.player.statistics.health_points / self.player.statistics.max_health_points) * 100
        self.render_text(self.string['hp'][1][0], self.string['hp'][1][2],
                         self.string['hp'][1][1], self.string['hp'][1][3], self.string['hp'][0])
        position = ((self.position[0] + 10) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    (self.position[1] + 30) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    ((380 / 100) * health_percent) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    20 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])

        self.rects_pos['hp'] = (position, (200, 0, 0))

        pygame.draw.rect(self.screen.screen, (200, 0, 0), position)

    def render_text(self, x1, x2, y1, y2, string):

        x = x2 - x1
        y = y2 - y1

        x /= 2
        y /= 2

        x += x1
        y += y1

        string = self.screen.font.render(string, self.screen.engine.settings.graphic['screen']['antialias'], (0, 0, 0))
        #self.screen.screen.blit(string, (x, y))

    def render(self):
        pygame.draw.rect(self.screen.screen, self.rects_pos['main'][1], self.rects_pos['main'][0])
        pygame.draw.rect(self.screen.screen, self.rects_pos['black_hp'][1], self.rects_pos['black_hp'][0])
        self.render_text(self.string['hp'][1][0], self.string['hp'][1][2],
                         self.string['hp'][1][1], self.string['hp'][1][3], self.string['hp'][0])
        health_percent = (self.player.statistics.health_points / self.player.statistics.max_health_points) * 100
        position = ((self.position[0] + 10) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    (self.position[1] + 10) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    ((380 / 100) * health_percent) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    20 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        pygame.draw.rect(self.screen.screen, (200, 0, 0), position)
