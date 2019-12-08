import pygame
from .gui_abstract_object import GuiAbstractObject


class BottomPanel(GuiAbstractObject):

    def __init__(self, x, y, player, screen):
        self.player = player
        self.position = (x, y, 1200, 125)
        self.screen = screen
        self.rects_pos = {
            'main': None,
        }
        self.buttons = []

    def create(self):
        position = (self.position[0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    self.position[2] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    self.position[3] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.rects_pos['main'] = (position, (255, 255, 255))

    def render(self):
        pygame.draw.rect(self.screen.screen, self.rects_pos['main'][1], self.rects_pos['main'][0])

    
