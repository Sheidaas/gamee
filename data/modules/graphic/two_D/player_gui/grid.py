import pygame


class Grid:

    def __init__(self):
        self.x = []
        self.y = []

    def create(self, screen):
        size = (75 * screen.engine.settings.graphic['screen']['resolution_scale'][0],
                75 * screen.engine.settings.graphic['screen']['resolution_scale'][1])
        start = (-10, -15)

        for x in range(20):
            start_position = (start[0] + (x * size[0]), 0)
            end_position = (start_position[0], screen.engine.settings.graphic['screen']['resolution_y'])
            self.x.append((start_position, end_position))

        for y in range(20):
            start_position = (0, start[1] + (y * size[1]))
            end_position = (screen.engine.settings.graphic['screen']['resolution_x'], start_position[1])
            self.y.append((start_position, end_position))

    def render(self, screen):
        for pos in self.x:
            pygame.draw.aaline(screen.screen, (0, 0, 0), pos[0], pos[1])

        for pos in self.y:
            pygame.draw.aaline(screen.screen, (0, 0, 0), pos[0], pos[1])
