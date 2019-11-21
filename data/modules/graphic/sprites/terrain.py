import pygame


class TerrainSprite(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_id = 0
        self.small_position = (0, 0)
        self.big_position = (0, 0)
