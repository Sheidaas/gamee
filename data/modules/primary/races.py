from data.modules.primary.statistics import Modifier
import json
import collections


class Race:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.description = ''
        self.relations = {}
        self.modifier = Modifier()
        self.abilities = []

    def add_modifier_to_statistics(self, statistic):
        statistic.modifiers.add_modifier(self.modifier)

    def add_skills_to_abilities(self, abilities, database):
        for skill_id in self.abilities:
            abilities.add_ability( database.return_race_by_id(skill_id) )


class RaceDatabases:

    def __init__(self, path: str, language: dict):
        self.races = []
        self.racesFileDestination = path + '/data/data' + '/races_file.json'

    def new_id(self):
        index = 1
        for race in self.races:
            index += 1
        return index

    def return_race_by_id(self, race_id):
        for race in self.races:
            if race.id == race_id:
                return race

    def add_race(self, race):
        race.id = self.new_id()
        self.races.append(race)

    def create_race(self, races_dict):
        for race in races_dict:
            r = Race()
            r.name = races_dict[race]['name']
            r.description = races_dict[race]['description']
            r.relations = races_dict[race]['relations']
            r.abilities = races_dict[race]['skills']
            r.modifier.name = races_dict[race]['modifier']['name']
            r.modifier.description = races_dict[race]['modifier']['description']
            r.modifier.effects = races_dict[race]['modifier']['effects']
            r.modifier.effects_permanently = True
            self.add_race(r)

    def init_database(self):
        with open(self.racesFileDestination, 'r') as file:
            data = file.read()
            races_dict = json.loads(data, object_pairs_hook=collections.OrderedDict)
        self.create_race(races_dict)

