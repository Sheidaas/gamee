import pygame


class Background:

    def __init__(self, x1, y1, x2, y2, color: tuple, screen):
        self.size = (x1 * screen.engine.settings.graphic['screen']['resolution_scale'][0],
                     y1 * screen.engine.settings.graphic['screen']['resolution_scale'][1],
                     x2 * screen.engine.settings.graphic['screen']['resolution_scale'][0],
                     y2 * screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.color = color
        self.rect = None
        self.screen = screen

    def render_background(self):
        pygame.draw.rect(self.screen.screen, self.color, self.size)
