from data.modules.primary.statistics import Modifier


class Item:
    def __init__(self):
        self.id = 0
        self.image = None
        self.type = ''
        self.name = ''
        self.description = ''
        self.value = 0
        self.weight = 0.0

    def __str__(self):
        return self.name


class ItemToWear(Item):

    def __init__(self):
        super().__init__()
        self.requirements = {
            'level': 0,
            'strength': 0,
            'agility': 0,
            'observation': 0,
        }
        self.founded = False


class Weapon(ItemToWear):

    def __init__(self):
        super().__init__()
        self.min_damage = 0
        self.max_damage = 0
        self.range = 1
        self.one_handed = True

class Sword(Weapon):

    def __init__(self):
        super().__init__()
        self.type = 'Sword'

    def slash(self):
        pass


class Armor(ItemToWear):

    def __init__(self):
        super().__init__()
        self.armor = 0


class BodyArmor(Armor):

    def __init__(self):
        super().__init__()
        self.type = 'BodyArmor'


class Boots(Armor):

    def __init__(self):
        super().__init__()
        self.type = 'Boots'


class Helmet(Armor):

    def __init__(self):
        super().__init__()
        self.type = 'Helmet'


class Gloves(Armor):

    def __init__(self):
        super().__init__()
        self.type = 'Gloves'


class Leggings(Armor):

    def __init__(self):
        super().__init__()
        self.type = 'Leggings'


class Modulator(ItemToWear):

    def __init__(self):
        super().__init__()
        self.type = 'Modulator'
        self.modifier = Modifier()
        self.modifier.effects_permanently = True


class Potion(Item):

    def __init__(self):
        super().__init__()
        self.type = 'Potion'
        self.modifier = Modifier()
        self.modifier.every_turn = True

    def explode(self):
        pass

