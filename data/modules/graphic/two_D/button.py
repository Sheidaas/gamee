import pygame


class Button:

    def __init__(self, start_x: int, start_y: int, size_x: int, size_y: int, string: str, font, func, screen,
                 settings, *kwargs):
        self.start = (start_x * settings['resolution_scale'][0], start_y * settings['resolution_scale'][1])
        self.size = (size_x * settings['resolution_scale'][0], size_y * settings['resolution_scale'][1])
        self.string = (string, font)
        self.function = func
        self.screen = screen
        self.settings = settings
        self.kwargs = kwargs

    def render_button(self):
        self.is_size_agree_for_font()
        self.render_rect()
        self.render_text()

    def render_text(self):
        text_size = self.string[1].size(self.string[0])

        x = self.size[0] - text_size[0]
        y = self.size[1] - text_size[1]

        x /= 2
        y /= 2

        x += self.start[0]
        y += self.start[1]

        text_to_render = self.string[1].render(self.string[0], int(self.settings['antialias']), (255, 255, 255))
        self.screen.blit(text_to_render, (x, y))

    def is_size_agree_for_font(self):
        text_size = self.string[1].size(self.string[0])

        new_size = []
        if self.size[0] < text_size[0]:
            new_size.append(text_size[0])
        else:
            new_size.append(self.size[0])

        if self.size[1] < text_size[1]:
            new_size.append(text_size[1])
        else:
            new_size.append(self.size[1])

        self.size = (new_size[0], new_size[1])

    def render_rect(self):
        pygame.draw.rect(self.screen, (100, 100, 100), (self.start[0], self.start[1], self.size[0], self.size[1]))

    def on_click(self):
        if self.function == None:
            self.function = lambda x: x
        self.function(*self.kwargs)