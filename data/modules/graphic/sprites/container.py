import pygame


class ContainerSprite(pygame.sprite.DirtySprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.small_position = (0, 0)
        self.big_position = (0, 0)
