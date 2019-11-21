class ObjectOnMap:

    def __init__(self):
        self.coordinate = []
        self.name = ''


class Chest(ObjectOnMap):

    def __init__(self):
        super().__init__()
        self.content = []

    def add_item_to_content(self, item):
        item.id = self.new_id()
        self.content.append(item)

    def new_id(self):
        index = 1
        for item in self.content:
            index += 1
        return index

    def remove_item_from_content(self, item_id):
        try:
            for item in self.content:
                if item.id == item_id:
                    self.content.remove(item)
                    break
        except IndexError:
            print("Index error when removing item from chest content")

    def give_away_all_items(self, person):
        items_to_remove = []
        for item in self.content:
            if person.equipment.add_item_to_inventory(item):
                items_to_remove.append(item)
        for item in items_to_remove:
            self.remove_item_from_content(item.id)

    def give_away_item(self, person, item):
        if person.equipment.add_item_to_inventory(item):
            self.remove_item_from_content(item.id)


class ItemsAtFloor(Chest):

    def __init__(self):
        super().__init__()


