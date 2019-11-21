from data.modules.primary import items
from copy import deepcopy


class Equipment:

    def __init__(self, statistics):
        self.statistics = statistics
        self.dressed_armor = {
            'left-hand': None,
            'right-hand': None,
            'head': None,
            'modulator': None,
            'body': None,
            'hands': None,
            'legs': None,
            'foots': None
        }
        self.inventory = []
        self.equipment_weight = 0
        self.equipment_max_weight = 60

    def change_equipment_weight(self, value):
        self.equipment_weight += value

    def calculate_equipment_max_weight(self):
        value = 0
        self.set_equipment_max_weight(value)

    def set_equipment_max_weight(self, value):
        self.equipment_max_weight = value

    def add_item_to_inventory(self, item, add_weight=True):
        if add_weight:
            if item.weight + self.equipment_weight <= self.equipment_max_weight:
                self.change_equipment_weight(round(item.weight, 3))

                for stack in self.inventory:
                    if item.id is stack.item.id:
                        stack.add_item(item)
                        return True

                item_stack = ItemStack(item)
                item_stack.add_item(item)
                self.inventory.append(item_stack)
                return True

            return False

        else:
            for stack in self.inventory:
                if item.id is stack.item.id:
                    stack.add_item(item)
                    return True

            item_stack = ItemStack(item)
            item_stack.add_item(item)
            self.inventory.append(item_stack)
            return True

    def remove_item_from_inventory(self, item_id):
        try:
            for stack in self.inventory:
                if stack.item.id == item_id:
                    self.change_equipment_weight(-stack.item.weight)
                    stack.return_item()

                    if stack.items_amount == 0:
                        self.inventory.remove(stack)
                    break
        except IndexError:
            print('Index error when removing ItemStack from inventory')

    def check_item_requirements_to_dress_up(self, item):
        if item.requirements['level'] <= self.statistics.level and \
            item.requirements['strength'] <= self.statistics.strength and \
            item.requirements['agility'] <= self.statistics.agility and \
            item.requirements['observation'] <= self.statistics.observation and \
            item.founded is False:
            return True
        return False

    def dress_up_item(self, item):
        _item = deepcopy(item.item)
        if self.check_item_requirements_to_dress_up(_item):
            _item.founded = True
            if isinstance(_item, items.Weapon):
                if _item.one_handed:
                    if self.dressed_armor['right-hand'] is not None:
                            if self.dressed_armor['left-hand'] is not None:
                                self.dress_off_item(self.dressed_armor['left-hand'], 'left-hand')
                            self.dressed_armor['left-hand'] = _item
                    else:
                        self.dressed_armor['right-hand'] = _item
                else:
                    if self.dressed_armor['left-hand'] is not None:
                        self.dress_off_item(self.dressed_armor['left-hand'], 'left-hand')
                    if self.dressed_armor['right-hand'] is not None:
                        self.dress_off_item(self.dressed_armor['right-hand'], 'right-hand')

                    self.dressed_armor['right-hand'] = _item
                    self.dressed_armor['left-hand'] = _item

                self.statistics.change_min_damage_by_value(_item.min_damage)
                self.statistics.change_max_damage_by_value(_item.max_damage)

            elif isinstance(_item, items.BodyArmor):
                if self.dressed_armor['body'] is not None:
                    self.dress_off_item(self.dressed_armor['body'], 'body')
                self.dressed_armor['body'] = _item

                self.statistics.change_armor_by_value(_item.armor)

            elif isinstance(_item, items.Boots):
                if self.dressed_armor['foots'] is not None:
                    self.dress_off_item(self.dressed_armor['foots'], 'foots')
                self.dressed_armor['foots'] = _item

                self.statistics.change_armor_by_value(_item.armor)

            elif isinstance(_item, items.Helmet):
                if self.dressed_armor['head'] is not None:
                    self.dress_off_item(self.dressed_armor['head'], 'head')
                self.dressed_armor['head'] = _item

                self.statistics.change_armor_by_value(_item.armor)

            elif isinstance(_item, items.Gloves):
                if self.dressed_armor['hands'] is not None:
                    self.dress_off_item(self.dressed_armor['hands'], 'hands')
                self.dressed_armor['hands'] = _item

                self.statistics.change_armor_by_value(_item.armor)

            elif isinstance(_item, items.Leggings):
                if self.dressed_armor['foots'] is not None:
                    self.dress_off_item(self.dressed_armor['legs'], 'legs')
                self.dressed_armor['legs'] = _item

                self.statistics.change_armor_by_value(_item.armor)

            elif isinstance(_item, items.Modulator):
                if self.dressed_armor['modulator'] is not None:
                    self.dress_off_item(self.dressed_armor['modulator'], 'modulator')
                self.dressed_armor['modulator'] = _item
                self.statistics.modifiers.add_modifier(_item.modifier)

            for stack in self.inventory:
                if _item.id == stack.item.id:
                    stack.subtract_item()
                    if not stack.check_stack():
                        self.inventory.remove(stack)
                    break

        else:
            print('Cannot equip item')

    def dress_off_item(self, item, key):
        if isinstance(item, items.Weapon):
            if item.one_handed:
                self.dressed_armor[key] = None
            else:
                self.dressed_armor['right-hand'] = None
                self.dressed_armor['left-hand'] = None

            self.statistics.change_min_damage_by_value(-item.min_damage)
            self.statistics.change_max_damage_by_value(-item.max_damage)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.BodyArmor):
            self.dressed_armor['body'] = None
            self.statistics.change_armor_by_value(-item.armor)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.Boots):
            self.dressed_armor['foots'] = None
            self.statistics.change_armor_by_value(-item.armor)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.Helmet):
            self.dressed_armor['head'] = None
            self.statistics.change_armor_by_value(-item.armor)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.Gloves):
            self.dressed_armor['hands'] = None
            self.statistics.change_armor_by_value(-item.armor)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.Leggings):
            self.dressed_armor['legs'] = None
            self.statistics.change_armor_by_value(-item.armor)
            item.founded = False
            self.add_item_to_inventory(item, False)

        elif isinstance(item, items.Modulator):
            self.dressed_armor['modulator'] = None
            self.statistics.modifiers.delete_modifier(item.modifier)
            item.founded = False
            self.add_item_to_inventory(item, False)


        else:
            print('Cannot deequip item')

    def return_stack(self, item_id):
        for stack in self.inventory:
            if item_id == stack.item.id:
                return stack
        return None

    def drink_potion(self, item):
        self.statistics.modifiers.add_modifier(deepcopy(item.modifier))
        self.remove_item_from_inventory(item.id)


class ItemStack:

    def __init__(self, item):
        self.id = item.id
        self.item = item
        self.items_amount = 0

    def set_id(self, value):
        self.id = value

    def add_item(self, item):
        self.set_id(item.id)
        self.items_amount += 1

    def subtract_item(self):
        if self.items_amount:
            self.items_amount -= 1

    def check_stack(self):
        if not self.items_amount:
            return False
        return True

    def return_item(self):
        self.items_amount -= 1
        return self.item

    def __str__(self):
        return str(self.item.id) + ' |' + self.item.name + '| ' + str(self.items_amount)

    def __len__(self):
        return self.items_amount
