from data.modules.primary.persons import Person
from collections import OrderedDict
import json
import copy


class Database:

    def __init__(self,path: str):
        self.persons = []
        self.fileDestination = path + '/data/data/' + 'persons_file.json'

    def select_person_by_id(self, id):
        for person in self.persons:
            if person.id == id:
                return person

    def new_id(self):
        index = 1
        for person in self.persons:
            index += 1
        return index

    def create_persons(self, persons_data, race_database, item_database, abilities_database):
        from data.modules.primary.statistics import Modifier
        for person in persons_data:
            p = Person()
            p.id = self.new_id()
            p.name = persons_data[person]['name']
            p.last_name = persons_data[person]['last_name']
            p.age = persons_data[person]['age']
            p.gender = persons_data[person]['gender']
            p.race = race_database.return_race_by_id(persons_data[person]['race'])
            p.portrait = persons_data[person]['portrait']
            p.coordinate = persons_data[person]['coordinate']
            p.location = persons_data[person]['location']
            p.map_sprite = persons_data[person]['map_sprite']
            p.statistics.health_points = persons_data[person]['statistics']['health_points']
            p.statistics.max_health_points = persons_data[person]['statistics']['max_health_points']
            p.statistics.experience = persons_data[person]['statistics']['experience']
            p.statistics.experience_to_next_level = persons_data[person]['statistics']['experience_to_next_level']
            p.statistics.level = persons_data[person]['statistics']['level']
            p.statistics.strength = persons_data[person]['statistics']['strength']
            p.statistics.agility = persons_data[person]['statistics']['agility']
            p.statistics.observation = persons_data[person]['statistics']['observation']
            p.statistics.luck = persons_data[person]['statistics']['luck']
            p.statistics.sight = persons_data[person]['statistics']['sight']
            p.statistics.chance_to_deflection = persons_data[person]['statistics']['chance_to_deflection']
            p.statistics.chance_to_block = persons_data[person]['statistics']['chance_to_block']
            p.statistics.chance_to_dodge = persons_data[person]['statistics']['chance_to_dodge']
            p.statistics.chance_to_critical_hit = persons_data[person]['statistics']['chance_to_critical_hit']
            p.statistics.critical_hit_power = persons_data[person]['statistics']['critical_hit_power']

            for modifier in persons_data[person]['statistics']['modifiers']:
                m = Modifier()
                m.name = modifier['name']
                m.description = modifier['description']
                m.turns_to_end = modifier['turns_to_end']
                m.every_turn = modifier['every_turn']
                m.effects = modifier['effects']
                m.effects_working = modifier['is_working']
                m.effects_permanently = modifier['is_permanently']
                p.statistics.modifiers.add_modifier(m)

            for item in persons_data[person]['equipment']['dressed_armor']:
                if persons_data[person]['equipment']['dressed_armor'][item] is not None:
                    p.equipment.dressed_armor[item] = copy.deepcopy(item_database.return_item_by_id(persons_data[person]['equipment']['dressed_armor'][item]))
                    p.equipment.dressed_armor[item].founded = True

            for item in persons_data[person]['equipment']['inventory']:
                p.equipment.add_item_to_inventory(item_database.return_item_by_id(item))

            for ability in persons_data[person]['abilities']:
                p.abilities.add_ability(abilities_database.return_ability_by_id(ability))

            self.add_person(p)

    def add_person(self, person):
        if isinstance(person, Person):
            self.persons.append(person)
        else:
            print('Tried to add no-person object to database')

    def save_persons(self):
        persons_to_save = {}
        for person in self.persons:
            person_dict = {
                'name': person.name,
                'last_name': person.last_name,
                'age': person.age,
                'gender': person.gender,
                'portrait': person.portrait,
                'race': person.race.id,
                'map_sprite': person.map_sprite,
                'location': person.location,
                'statistics': {
                    'health_points': person.statistics.health_points,
                    'max_health_points': person.statistics.max_health_points,
                    'experience': person.statistics.experience,
                    'experience_to_next_level': person.statistics.experience_to_next_level,
                    'level': person.statistics.level,
                    'strength': person.statistics.strength,
                    'agility': person.statistics.agility,
                    'observation': person.statistics.observation,
                    'luck': person.statistics.luck,
                    'sight': person.statistics.sight,
                    'chance_to_deflection': person.statistics.chance_to_deflection,
                    'chance_to_block': person.statistics.chance_to_block,
                    'chance_to_dodge': person.statistics.chance_to_dodge,
                    'chance_to_critical_hit': person.statistics.chance_to_critical_hit,
                    'critical_hit_power': person.statistics.critical_hit_power,
                },
                'equipment': {
                    'dressed_armor': {},
                    'inventory': [],
                    'equipment_weight': person.equipment.equipment_weight
                },
                'coordinate': person.coordinate,
                'abilities': person.return_abilities_id_to_list()
            }

            modifiers = []
            for effect in person.statistics.modifiers.modifiers:
                effect_dict = {
                    'name': effect.name,
                    'description': effect.description,
                    'turns_to_end': effect.turns_to_end,
                    'every_turn': effect.every_turn,
                    'effects': effect.effects,
                    'is_working': effect.effects_working,
                    'is_permanently': effect.effects_permanently
                }
                modifiers.append(effect_dict)
            person_dict['statistics']['modifiers'] = modifiers
            del modifiers

            for item in person.equipment.dressed_armor:
                if person.equipment.dressed_armor[item] is not None:
                    person_dict['equipment']['dressed_armor'][item] = person.equipment.dressed_armor[item].id
                else:
                    person_dict['equipment']['dressed_armor'][item] = None

            items = []
            for item_stack in person.equipment.inventory:
                for idx in range(item_stack.items_amount):
                    items.append(item_stack.id)
            person_dict['equipment']['inventory'] = items
            del items

            abilities = [idx.id for idx in person.abilities.abilities]
            person_dict['abilities'] = abilities
            del abilities

            persons_to_save[person.id] = person_dict
        return persons_to_save

    def save_persons_file(self, destination=''):
        path = ''
        if destination: path = destination
        else: path = self.fileDestination
        with open(path, 'w') as file:
            file.write(json.dumps(self.save_persons(), indent=4))

    def init_database(self, races_database, items_database, abilities_database, state_destination=''):
        file_path = ''
        if state_destination: file_path = state_destination
        else: file_path = self.fileDestination
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                persons_data = json.loads(data, object_pairs_hook=OrderedDict)

                self.create_persons(persons_data, races_database, items_database, abilities_database)
        except IOError:
            print('File doesnt exist')
