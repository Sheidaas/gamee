from data.modules.primary.statistics import Modifier
import random


class Database:
    def __init__(self):
        self.abilities = []

    def return_ability_by_id(self, ability_id):
        for ability in self.abilities:
            if ability.id == ability_id:
                return ability

    def add_ability(self, ability):
        self.abilities.append(ability)

    def init_database(self):
        self.add_ability(Berserk())


class Berserk:

    def __init__(self):
        self.id = 0
        self.image_path = ('/data/graphic/abilities/berserk.png')
        self.experience = 0
        self.level = 1
        self.max_level = 10
        self.type = 'strengthening'
        self.is_passive = False
        self.name = 'Berserk'
        self.description = 'Work in progress'
        self.time_to_renew = 7
        self.time_of_action = 3
        self.requirements = {
            'level': 1,
            'strength': 6,
            'agility': 4,
            'observation': 0,
            'profession': '',
        }
        self.working_upgrade = {
            'strength': 4,
            'agility': 2,
            'observation': -2
        }

    def change_experience_by_value(self, value):
        self.experience += value
        if value > 0:
            self.check_experience()

    def check_experience(self):
        while True:
            if self.experience >= self.level * 800:
                self.level_up()
            else:
                break

    def level_up(self):
        self.level += 1
        self.time_of_action += 1
        self.working_upgrade['strength'] += 2
        self.working_upgrade['agility'] += 1
        self.working_upgrade['observation'] += 1

    def use_ability(self):
        self.change_experience_by_value(random.randint(10, 80))
        modifier = Modifier()
        modifier.effects['strength'] = self.working_upgrade['strength']
        modifier.effects['agility'] = self.working_upgrade['agility']
        modifier.effects['observation'] = self.working_upgrade['observation']
        modifier.turns_to_end = self.time_of_action
        modifier.name = 'Berserk'
        modifier.description = 'ARGHHHH'
        return modifier
