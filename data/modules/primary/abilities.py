class Abilities:

    def __init__(self, statistics):
        self.abilities = []
        self.abilities_on_hub = {
            'key' """ keyboard_key """: int,  # ability_id
        }
        self.statistics = statistics

    def new_id(self):
        index = 0
        for ability in self.abilities:
            index += 1
        return index

    def add_ability(self, ability):
        ability.id = self.new_id()
        self.abilities.append(ability)

    def use_ability(self, id):
        for ability in self.abilities:
            if id == ability.id:
                modifier = ability.use_ability()
                self.statistics.modifiers.add_modifier(modifier)
                print('used ' + ability.name)

    def set_key_to_cast_ability(self, key, ability):
        self.abilities[key] = ability.id


