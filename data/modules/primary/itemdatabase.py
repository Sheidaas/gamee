from data.modules.primary import items
import json
import collections


class Database:

    def __init__(self, path: str, language: dict):
        self.items = []
        self.fileDestination = path + '/data/data/' + 'items_file.json'
        self.items_language = language

    def new_id(self):
        index = 1
        for item in self.items:
            index += 1
        return index

    def return_item_by_id(self, item_id: int):
        for item in self.items:
            if item.id == item_id:
                return item

    def add_item_to_database(self, item):
        item.id = self.new_id()
        self.items.append(item)
        self.save_items_file()

    def create_items(self, items_data: dict):
        for index in items_data:
            if items_data[index]['type'] == 'Sword':
                item = items.Sword()
                item.requirements = items_data[index]['requirements']
                item.min_damage = items_data[index]['min_damage']
                item.max_damage = items_data[index]['max_damage']
                item.range = items_data[index]['range']
                item.one_handed = items_data[index]['one_handed']

            elif items_data[index]['type'] == 'BodyArmor':
                item = items.BodyArmor()
                item.requirements = items_data[index]['requirements']
                item.armor = items_data[index]['armor']

            elif items_data[index]['type'] == 'Boots':
                item = items.Boots()
                item.requirements = items_data[index]['requirements']
                item.armor = items_data[index]['armor']

            elif items_data[index]['type'] == 'Helmet':
                item = items.Helmet()
                item.requirements = items_data[index]['requirements']
                item.armor = items_data[index]['armor']

            elif items_data[index]['type'] == 'Gloves':
                item = items.Gloves()
                item.requirements = items_data[index]['requirements']
                item.armor = items_data[index]['armor']

            elif items_data[index]['type'] == 'Leggings':
                item = items.Leggings
                item.requirements = items_data[index]['requirements']
                item.armor = items_data[index]['armor']

            elif items_data[index]['type'] == 'Modulator':
                item = items.Modulator()
                item.modifier.name = self.items_language['items'][index]['modifier']['name']
                item.requirements = items_data[index]['requirements']
                item.modifier.description = self.items_language['items'][index]['modifier']['description']
                item.modifier.effects = items_data[index]['modifier']['effects']

            elif items_data[index]['type'] == 'Potion':
                item = items.Potion()
                item.modifier.name = self.items_language['items'][index]['modifier']['name']
                item.modifier.description = self.items_language['items'][index]['modifier']['description']
                item.modifier.effects = items_data[index]['modifier']['effects']
                item.modifier.turns_to_end = items_data[index]['modifier']['turns_to_end']
                item.modifier.every_turn = items_data[index]['modifier']['every_turn']

            item.name = self.items_language['items'][index]['name']
            item.type = items_data[index]['type']
            item.description = self.items_language['items'][index]['description']
            item.value = items_data[index]['value']
            item.weight = items_data[index]['weight']
            item.image = items_data[index]['image']

            self.add_item_to_database(item)

    def save_items(self):
        items_dict = {}
        for item in self.items:
            item_dict = {
                    'type': item.type,
                    'value': item.value,
                    'weight': item.weight,
                    'image': item.image
            }
            if item.type == 'Sword':
                item_dict['requirements'] = item.requirements
                item_dict['founded'] = item.founded
                item_dict['min_damage'] = item.min_damage
                item_dict['max_damage'] = item.max_damage
                item_dict['range'] = item.range
                item_dict['one_handed'] = item.one_handed

            if item.type == 'Modulator':
                item_dict['requirements'] = item.requirements
                item_dict['founded'] = item.founded
                item_dict['modifier'] = {
                    'effects': item.modifier.effects
                }

            if item.type == 'Potion':
                item_dict['modifier'] = {
                    'every_turn': item.modifier.every_turn,
                    'turns_to_end': item.modifier.turns_to_end,
                    'effects': item.modifier.effects
                }

            if isinstance(item, items.Armor):
                item_dict['requirements'] = item.requirements
                item_dict['founded'] = item.founded
                item_dict['armor'] = item.armor

            items_dict[item.id] = item_dict

        return items_dict

    def save_items_file(self):
        with open(self.fileDestination, 'w') as file:
            data = json.dumps(self.save_items(), indent=4)
            file.write(data)

    def init_database(self):
        try:
            with open(self.fileDestination, 'r') as file:
                data = file.read()
                items_data = json.loads(data, object_pairs_hook=collections.OrderedDict)
            self.create_items(items_data)
        except FileExistsError:
            print('item database file doesnt exist')
