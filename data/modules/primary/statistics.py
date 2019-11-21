class Statistics:

    def __init__(self):
        self.health_points = 0
        self.max_health_points = 0

        self.experience = 500
        self.experience_to_next_level = 800
        self.level = 0

        self.min_damage = 0
        self.max_damage = 0

        self.armor = 0

        self.strength = 0
        self.agility = 0
        self.observation = 0
        self.charisma = 0
        self.luck = 0
        self.sight = 0

        self.chance_to_deflection = 0.0
        self.chance_to_block = 0.0
        self.chance_to_dodge = 0.0

        self.chance_to_critical_hit = 0.0
        self.critical_hit_power = 1.5

        self.modifiers = Modifiers(self)

    def change_strength_by_value(self, value):
        self.strength += value

    def change_agility_by_value(self, value):
        self.agility += value

    def change_observation_by_value(self, value):
        self.observation += value

    def change_charisma_by_value(self, value):
        self.charisma += value

    def change_luck_by_value(self, value):
        self.luck += value

    def change_sight_by_value(self, value):
        self.sight += value

    def change_chance_to_deflection_by_value(self, value):
        self.chance_to_deflection += value

    def change_chance_to_block_by_value(self, value):
        self.chance_to_block += value

    def change_chance_to_dodge_by_value(self, value):
        self.chance_to_dodge += value

    def change_chance_to_critical_hit_by_value(self, value):
        self.chance_to_critical_hit += value

    def change_critical_hit_power_by_value(self, value):
        self.critical_hit_power += value

    def change_experience_by_value(self, value):
        self.experience += value

    def change_level_by_value(self, value):
        self.level += value

    def change_min_damage_by_value(self, value):
        self.min_damage += value

    def change_max_damage_by_value(self, value):
        self.max_damage += value

    def change_armor_by_value(self, value):
        self.armor += value

    def change_health_points_by_value(self, value):
        if self.health_points + value > self.max_health_points:
            self.health_points += self.max_health_points - self.health_points
        else:
            self.health_points += value

    def change_max_health_points_by_value(self, value):
        self.max_health_points += value


class Modifiers:

    def __init__(self, statistics):
        self.statistics = statistics
        self.modifiers = []

    def change_statistics(self):
        modifiers_index_to_delete = []

        for effect in self.modifiers:
            if effect.effects_working is False and effect.effects_permanently is False and effect.turns_to_end > 0:
                for key in effect.effects.keys():
                    getattr(self.statistics, str('change_' + key + '_by_value'))(effect.effects[key])

                if effect.every_turn:
                    effect.turns_to_end -= 1
                else:
                    effect.effects_working = True
                    effect.turns_to_end -= 1

            elif effect.effects_working and effect.effects_permanently is False and effect.turns_to_end > 0:

                effect.turns_to_end -= 1

            elif effect.effects_permanently is False and effect.turns_to_end == 0:

                for key in effect.effects.keys():

                    getattr(self.statistics, str('change_' + key + '_by_value'))(-effect.effects[key])

                modifiers_index_to_delete.append(effect.id)

            elif effect.effects_permanently and effect.effects_working is False:

                for key in effect.effects.keys():
                    getattr(self.statistics, str('change_' + key + '_by_value'))(effect.effects[key])

                effect.effects_working = True

        self.delete_a_lot_modifiers(modifiers_index_to_delete)

    def delete_a_lot_modifiers(self, modifiers_index_to_delete):
        for index in modifiers_index_to_delete:
            self.delete_modifier(index)

    def add_modifier(self, modifier):
        modifier.id = self.new_modifier_index()
        self.modifiers.append(modifier)

    def delete_modifier(self, modifier_index):
        try:
            for modifier in self.modifiers:
                if modifier.id == modifier_index:
                    self.modifiers.remove(modifier)
                    break
        except IndexError:
            print('Index error when delete_modifier')

    def return_modifier_using_object(self, modifier):
        for x in self.modifiers:
            if x == modifier:
                return x

    def new_modifier_index(self):
        index = 1
        for x in self.modifiers:
            index += 1
        return index


class Modifier:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.description = ''
        self.turns_to_end = 0
        self.every_turn = False
        self.effects = {
            'health_points': 0,
            'max_health_points': 0,
            'strength': 0,
            'agility': 0,
            'observation': 0,
            'charisma': 0,
            'luck': 0,
            'sight': 0,
            'chance_to_deflection': 0.0,
            'chance_to_block': 0.0,
            'chance_to_dodge': 0.0,
            'chance_to_critical_hit': 0.0,
            'critical_hit_power': 0.0
        }
        self.effects_working = False
        self.effects_permanently = False




