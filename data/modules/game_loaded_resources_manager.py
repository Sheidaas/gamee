import pygame
from data.modules.graphic.sprites.terrain import TerrainSprite
from data.modules.graphic.sprites.person import PersonSprite
from data.modules.graphic.image_modificator import resize_image


class LoadedResourcesMenager:

    def __init__(self, screen):
        self.screen = screen

        self.terrain_images = []
        self.terrain_sprites = pygame.sprite.Group()

        self.person_sprite_menager = pygame.sprite.Group()

        self.objects_sprite_menager = pygame.sprite.Group()

    def load_terrain(self, terrain, key, map):
        terrain_images = {
            'id': key,
            'image': resize_image(self.screen, terrain['sprite'])
        }
        size = terrain_images['image'].get_size()

        self.terrain_images.append(terrain_images)

        for y in range(len(map.map)):
            for x in range(len(map.map[y])):
                if map.map[y][x] == int(key):
                    terrain_sprite = TerrainSprite()
                    terrain_sprite.image_id = key
                    terrain_sprite.small_position = (x, y)
                    terrain_sprite.big_position = (x * size[0], y * size[1])
                    self.terrain_sprites.add(terrain_sprite)

    def get_terrain_sprite_by_small_position(self, small_position):
        for sprite in self.terrain_sprites.sprites():
            if sprite.small_position == small_position:
                return sprite

    def get_terrain_image_by_id(self, image_id):
        for terrain in self.terrain_images:
            if terrain['id'] == image_id:
                return terrain['image']

    def load_person(self, person, person_sprite):
        person_sprite.small_position = person.coordinate
        person_sprite.image = resize_image(self.screen, person_sprite.image)
        size = person_sprite.image.get_size()
        person_sprite.big_position = (person.coordinate[0] * size[0], person.coordinate[1] * size[1])
        self.person_sprite_menager.add(person_sprite)

    def update_person_sprite_positions(self, old_move, new_move):
        pass

    def get_person_sprite_by_person_id(self, person_id):
        for sprite in self.person_sprite_menager.sprites():
            if sprite.person_id == person_id:
                return sprite

    def get_person_sprite_by_small_position(self, small_position):
        for sprite in self.person_sprite_menager.sprites():
            if sprite.small_position == tuple(small_position):
                return sprite

    def load_object(self, object, object_sprite):
        object_sprite.small_position = object.coordinate
        object_sprite.image = resize_image(self.screen, object_sprite.image)
        size = object_sprite.image.get_size()
        object_sprite.big_position = (object.coordinate[0] * size[0], object.coordinate[1] * size[1])
        self.objects_sprite_menager.add(object_sprite)

    def get_object_sprite_by_small_position(self, small_position):
        for sprite in self.objects_sprite_menager.sprites():
            if tuple(sprite.small_position) == small_position:
                return sprite
