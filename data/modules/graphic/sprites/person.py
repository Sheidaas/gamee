import pygame


class PersonSprite(pygame.sprite.DirtySprite):

    def __init__(self, image, person_id):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.person_id = person_id
        self.small_position = (0, 0)
        self.big_position = (0, 0)
