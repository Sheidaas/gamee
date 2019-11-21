import pygame


class Location:

    def __init__(self, x, y, player, screen):
        self.player = player
        self.position = (x, y, 400, 30)
        self.screen = screen
        self.rects_pos = {
            'main': None,
        }
        self.strings = {
            'location': (),
        }
        self.buttons = []

    def create(self):
        position = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[1] - 100 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    self.position[2] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[3] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.rects_pos['main'] = (position, (255, 255, 255))

        text = self.screen.engine.map.name + ' | x: ' + str(self.player.coordinate[0]) + ' | y: '\
               + str(self.player.coordinate[1])
        self.strings['location'] = (text, position)


    def render(self):
        pygame.draw.rect(self.screen.screen, self.rects_pos['main'][1], self.rects_pos['main'][0])
        text = self.screen.engine.map.name + ' | x: ' + str(self.player.coordinate[0]) + ' | y: '\
               + str(self.player.coordinate[1])
        self.strings['location'] = (text, self.strings['location'][1])
        self.render_text(self.strings['location'][1][0], self.strings['location'][1][2], self.strings['location'][1][1],
                         self.strings['location'][1][3], self.strings['location'][0])

    def render_text(self, x1, x2, y1, y2, string):
        text_size = self.screen.font.size(string)

        x = x2 - text_size[0]
        y = y2 - text_size[1]

        x /= 2
        y /= 2

        x += x1
        y += y1

        string = self.screen.font.render(string, self.screen.engine.settings.graphic['screen']['antialias'], (0, 0, 0))
        self.screen.screen.blit(string, (x, y))
