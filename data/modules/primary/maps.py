import json
import pygame
from data.modules.primary import objects
from data.modules.graphic.sprites.person import PersonSprite
from data.modules.graphic.sprites.container import ContainerSprite
from data.modules.graphic.sprites.terrain import TerrainSprite


class Map:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.map = {}
        self.resources = {}
        self.size = {
            'x': 0,
            'y': 0
        }
        self.persons = []
        self.objects = {}

        self.resources_in_dict = {}

class MapLoader:

    def __init__(self, real_path: str, file_path: str):
        self.path = real_path
        self.file_destination = file_path

    def return_map(self, person_db, item_db, loadedresourcesmenager):
        json_map = self.load_map_from_file()
        map = Map()

        map.id = json_map['id']
        map.name = json_map['name']
        map.map = json_map['map']

        for key in json_map['resources']:
            map.resources[key] = json_map['resources'][key]
            map.resources_in_dict[key] = json_map['resources'][key]
        self.load_resources(map, loadedresourcesmenager)

        for key in json_map['objects']:
            map.objects[key] = json_map['objects'][key]
        self.load_objects(map, item_db, loadedresourcesmenager)

        for idx in json_map['persons']:
            map.persons.append(idx)
            person = person_db.select_person_by_id(idx)
            person_sprite = PersonSprite(pygame.image.load(self.path + '/data/graphic/sprites/' + person.map_sprite), person.id)
            loadedresourcesmenager.load_person(person, person_sprite)

        map.size['x'] = len(map.map[0])
        map.size['y'] = len(map.map)
        return map

    def load_resources(self, map, loadedresourcesmenager):
        for key in map.resources.keys():
            map.resources[key]['sprite'] = pygame.image.load(self.path + '/' + map.resources[key]['sprite'])
            loadedresourcesmenager.load_terrain(map.resources[key], key, map)

    def load_objects(self, map, item_db, loadedresourcesmenager):
        for key in map.objects.keys():
            if map.objects[key]['name'] == 'chest':
                map.objects[key]['object'] = objects.Chest()
                map.objects[key]['object'].coordinate = [map.objects[key]['coordinate']['x'],
                                                         map.objects[key]['coordinate']['y']]
                map.objects[key]['object'].name = 'chest'
                for index in map.objects[key]['content']:
                    map.objects[key]['object'].content.append(
                        item_db.return_item_by_id(map.objects[key]['content'][index]))

                map.objects[key].pop('content', None)
                map.objects[key].pop('coordinate', None)
            if map.objects[key]['name'] == 'tree':
                map.objects[key]['object'] = objects.ObjectOnMap()
                map.objects[key]['object'].coordinate = [map.objects[key]['coordinate']['x'],
                                                         map.objects[key]['coordinate']['y']]

            loadedresourcesmenager.load_object(map.objects[key]['object'], ContainerSprite(pygame.image.load(self.path + '/' + map.objects[key]['sprite'])))


    def load_map_from_file(self):
        with open(self.file_destination, 'r') as file:
            return json.loads(file.read())

class MapSaver:

    def save_map(self, map: Map, path):
        dict_to_save = {
            'id': map.id,
            'name': map.name,
            'map': map.map,
            'persons': self.save_persons(map),
            'resources': self.save_resources(map),
            'objects': self.save_objects(map),
        }
        self.save_to_file(dict_to_save, path)

    def save_objects(self, map: Map):
        dict_to_save = {}
        map_objects_saver = MapObjectsSaver()
        for key in map.objects.keys():
            if map.objects[key]['type'] == 'container':
                dict_to_save[key] = map_objects_saver.save_container(map.objects[key])
        return dict_to_save

    def save_resources(self, map: Map):
        dict_to_save = {}
        for key in map.resources_in_dict.keys():
            dict_to_save[key] = {
                'sprite': map.resources_in_dict[key]['path_to_sprite'],
                'path_to_sprite': map.resources_in_dict[key]['path_to_sprite'],
                'name': map.resources_in_dict[key]['name'],
                'can_walk': map.resources_in_dict[key]['can_walk']
            }
        return dict_to_save

    def save_persons(self, map: Map):
        return map.persons

    def save_to_file(self, dict, path):
        with open(path, 'w') as file:
            file.write(json.dumps(dict, sort_keys=True, indent=4))


class MapObjectsSaver:

    def save_container(self, _dict: dict) -> dict:
        return {
            'type': 'container',
            'sprite': _dict['path_to_sprite'],
            'path_to_sprite': _dict['path_to_sprite'],
            'coordinate': {
                'x': _dict['object'].coordinate[0],
                'y': _dict['object'].coordinate[1],
            },
            'content': [idx.id for idx in _dict['object'].content],
            'name': _dict['name'],
            'can_walk': _dict['can_walk']
        }
