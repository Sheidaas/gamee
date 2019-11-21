from data.modules.graphic.two_D.button import Button
from data.modules.graphic.two_D.player_gui.container import Containter
from data.modules.graphic.two_D.player_gui.inventory import Inventory
from data.modules.graphic.two_D.player_gui.item_information import ItemInformation
from data.modules.primary import items


class Details:

    def __init__(self, screen, where_is_item, mouse_position):
        self.screen = screen
        self.where_is_item = where_is_item
        self.buttons = {}
        self.mouse_position = mouse_position

    def create(self):
        if self.where_is_item == 'container':
            self.buttons['take'] = (Button(self.mouse_position[0], self.mouse_position[1], 200, 50,
                                           self.screen.engine.database.language.texts['gui']['item_details']['take'],
                                           self.screen.font, self.take_item,
                                           self.screen.screen, self.screen.engine.settings.graphic['screen']))

            self.add_information_button(50)

        if self.where_is_item == 'inventory':


            if not isinstance(self.screen.game.drawer.gui['item_details']['item'], items.Potion):
                if not self.screen.game.drawer.gui['item_details']['item'].founded:
                    self.buttons['wear_up'] = (Button(self.mouse_position[0], self.mouse_position[1], 200, 50,
                                                   self.screen.engine.database.language.texts['gui']['item_details'][
                                                       'wear_up'],
                                                   self.screen.font, self.click_on_inventory_at_item,
                                                   self.screen.screen, self.screen.engine.settings.graphic['screen']))

                    self.add_information_button(100)
                else:
                    self.buttons['wear_off'] = (Button(self.mouse_position[0], self.mouse_position[1], 200, 50,
                                                   self.screen.engine.database.language.texts['gui']['item_details'][
                                                       'wear_off'],
                                                   self.screen.font, self.click_on_inventory_at_item,
                                                   self.screen.screen, self.screen.engine.settings.graphic['screen']))

                    self.add_information_button(100)



            elif isinstance(self.screen.game.drawer.gui['item_details']['item'], items.Potion):
                self.buttons['drink'] = (Button(self.mouse_position[0], self.mouse_position[1], 200, 50,
                                                  self.screen.engine.database.language.texts['gui']['item_details']['drink'],
                                                  self.screen.font, self.drink_potion,
                                                  self.screen.screen, self.screen.engine.settings.graphic['screen']))

                self.add_information_button(100)



            if self.screen.game.drawer.gui['container']['container'] != None:
                self.buttons['put_down'] = (Button(self.mouse_position[0], self.mouse_position[1] + 50, 200, 50,
                                                   self.screen.engine.database.language.texts['gui']['item_details'][
                                                       'put_down'],
                                                   self.screen.font, self.put_down_item,
                                                   self.screen.screen, self.screen.engine.settings.graphic['screen']))
            elif self.screen.game.drawer.gui['container']['container'] == None:
                self.buttons['drop'] = (Button(self.mouse_position[0], self.mouse_position[1] + 50, 200, 50,
                                               self.screen.engine.database.language.texts['gui']['item_details'][
                                                   'drop'],
                                               self.screen.font, None,
                                               self.screen.screen, self.screen.engine.settings.graphic['screen']))

    def render(self):
        for button in self.buttons:
            self.buttons[button].render_button()

    def add_information_button(self, y):
        self.buttons['information'] = (Button(self.mouse_position[0], self.mouse_position[1] + y, 200, 50,
                                       self.screen.engine.database.language.texts['gui']['item_details']['information'],
                                       self.screen.font, self.show_item_details,
                                       self.screen.screen, self.screen.engine.settings.graphic['screen']))

    def is_clicked_without_details(self, mouse_position):
        area = (self.mouse_position[0], self.mouse_position[1],
                self.mouse_position[0] + 200, self.mouse_position[1] + len(self.buttons) * 50)
        if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
            and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
            return True
        return False

    def click_on_inventory_at_item(self):
        self.screen.game.drawer.is_mouse_clicked_inventory('inventory', self.mouse_position, self.screen, 'left')

        self.screen.engine.next_turn()

        self.screen.game.gui['item_details'] = False
        self.screen.game.drawer.gui['item_details']['graphic_object'] = None
        self.screen.game.drawer.gui['item_details']['item'] = None

    def take_item(self):
        self.screen.game.drawer.is_mouse_clicked_container('container', self.mouse_position,
                                                      'left', self.screen.engine.return_player(), self.screen)
        self.screen.game.drawer.gui['container']['graphic_object'] = None
        self.screen.game.drawer.gui['container']['graphic_object'] = Containter(
            self.screen.game.drawer.gui['container']['container'], self.screen)
        self.screen.game.drawer.gui['container']['graphic_object'].create(self.screen, self.screen.engine.database.item_database)

        if self.screen.game.drawer.gui['player']['inventory'] != None:
            self.screen.game.drawer.gui['player']['inventory'] = Inventory(self.screen, self.screen.engine.return_player().equipment)
            self.screen.game.drawer.gui['player']['inventory'].create(self.screen, self.screen.engine.database.item_database)
            self.screen.game.drawer.gui['player']['inventory'].render()

        self.screen.game.gui['item_details'] = False
        self.screen.game.drawer.gui['item_details']['graphic_object'] = None
        self.screen.game.drawer.gui['item_details']['item'] = None

        self.screen.engine.next_turn()

    def put_down_item(self):
        for item in self.screen.game.drawer.gui['player']['inventory'].item_sprites:
            if self.screen.game.drawer.is_mouse_clicked_in_object_on_map(
                self.screen.game.drawer.gui['player']['inventory'].item_sprites[item],
                self.screen.game.drawer.gui['player']['inventory'].item_sprites[item]['position'],
                self.mouse_position, 'left'):

                _item = self.screen.game.drawer.gui['player']['inventory'].inventory.inventory[item].item
                self.screen.game.drawer.gui['player']['inventory'].inventory.remove_item_from_inventory(_item.id)
                self.screen.game.drawer.gui['container']['container'].add_item_to_content(_item)
                break

        self.screen.game.drawer.gui['player']['inventory'] = None
        self.screen.game.drawer.gui['container']['graphic_object'] = None
        self.screen.game.drawer.gui['container']['graphic_object'] = Containter(
            self.screen.game.drawer.gui['container']['container'], self.screen)
        self.screen.game.drawer.gui['container']['graphic_object'].create(self.screen, self.screen.engine.database.item_database)
        self.screen.game.drawer.gui['container']['graphic_object'].render()

        self.screen.game.drawer.gui['player']['inventory'] = Inventory(self.screen, self.screen.engine.return_player().equipment)
        self.screen.game.drawer.gui['player']['inventory'].create(self.screen, self.screen.engine.database.item_database)
        self.screen.game.drawer.gui['player']['inventory'].render()

        self.screen.game.gui['item_details'] = False
        self.screen.game.drawer.gui['item_details']['graphic'] = None
        self.screen.game.drawer.gui['item_details']['item'] = None

        self.screen.engine.next_turn()

    def show_item_details(self):
        item = self.screen.game.drawer.gui['item_details']['item']
        possibility = 0
        # if posilility == 0 then do nothing
        # if posibility == 1 then open inventory with container
        # if posibility == 2 then open container with inventory

        if self.where_is_item == 'inventory':
            self.screen.game.gui['inventory'] = False
            if self.screen.game.gui['container']:
                possibility = 1
                self.screen.game.gui['container'] = False

        if self.where_is_item == 'container':
            self.screen.game.gui['container'] = False

            if self.screen.game.gui['inventory']:
                possibility = 2
                self.screen.game.gui['inventory'] = False
                self.screen.game.drawer.gui['player']['inventory'] = None

        self.screen.game.gui['item_details'] = False
        self.screen.game.drawer.gui['item_details']['graphic_object'] = None
        self.screen.game.drawer.gui['item_details']['item'] = None

        self.screen.game.drawer.gui['item_information']['item'] = item
        self.screen.game.gui['item_information'] = True
        self.screen.game.drawer.gui['item_information']['graphic_object'] = ItemInformation(
            self.screen, self.where_is_item, possibility)
        self.screen.game.drawer.gui['item_information']['graphic_object'].create()

    def drink_potion(self):
        self.screen.game.drawer.gui['player']['inventory'].inventory.drink_potion(
            self.screen.drawer.gui['item_details']['item'])

        self.screen.game.drawer.gui['player']['inventory'] = Inventory(self.screen, self.screen.engine.return_player().equipment)
        self.screen.game.drawer.gui['player']['inventory'].create(self.screen, self.screen.engine.database.item_database)
        self.screen.game.drawer.gui['player']['inventory'].render()

        self.screen.game.gui['item_details'] = False
        self.screen.game.drawer.gui['item_details']['graphic'] = None
        self.screen.game.drawer.gui['item_details']['item'] = None

        self.screen.engine.next_turn()
