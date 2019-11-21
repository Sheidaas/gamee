import pygame


class Experience:

    def __init__(self, x, y, player, screen, absolutive_path):
        self.path = absolutive_path
        self.player = player
        self.position = (x, y, 1200, 30)
        self.screen = screen
        self.rects_pos = {
            'main': None,
            'progress': None,
        }
        self.abilities = []
        self.strings = {
            'experience': (),
        }
        self.buttons = []

    def create(self):
        position = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    self.position[2] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[3] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.rects_pos['main'] = (position, (255, 255, 255))
        self.strings['experience'] = ('', position)


    def render(self):
        exp_percent = (self.player.statistics.experience / self.player.statistics.experience_to_next_level) * 100
        position = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    ((self.position[2] / 100) * exp_percent) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[3] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.rects_pos['progress'] = (position, (240, 234, 45))

        for key in self.rects_pos.keys():
            pygame.draw.rect(self.screen.screen, self.rects_pos[key][1], self.rects_pos[key][0])

        text = str(self.player.statistics.experience) + '/' + str(self.player.statistics.experience_to_next_level)
        self.strings['experience'] = (text, self.strings['experience'][1])

        self.render_text(self.strings['experience'][1][0], self.strings['experience'][1][2], self.strings['experience'][1][1],
                         self.strings['experience'][1][3], self.strings['experience'][0])

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