from data.modules.graphic.two_D.button import Button
from data.modules.primary import items
from .gui_abstract_object import GuiAbstractObject
import pygame


class ItemInformation(GuiAbstractObject):

    def __init__(self, screen, where_is_item, possibility):
        self.buttons = {}
        self.sprites = {}
        self.texts = {}
        self.where_is_item = where_is_item
        self.screen = screen
        self.position = ()
        self.possibility = possibility

    def set_position(self):
        x = 560
        y = 50
        self.position = (x, y, 765, 500)

    def create(self):
        self.set_position()
        self.load_label_and_body()
        self.load_item_portrait()
        self.create_text()

        self.buttons['exit'] = Button(self.position[0] + 765, self.position[1] + 5, 30, 30, 'x', self.screen.font,
                                   self.exit_button, self.screen.screen, self.screen.engine.settings.graphic['screen'])

    def create_text(self):
        # Creating title
        text = self.screen.engine.database.language.texts['gui']['item_information']['title']
        text_size = self.screen.font.size(text)
        image_size = self.sprites['label']['sprite'].get_size()
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1]

        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['title'] = {}
        self.texts['title']['text'] = text
        self.texts['title']['render'] = text_to_render
        self.texts['title']['position'] = (x, y)


        item = self.screen.game.drawer.gui['item_information']['item']

        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1])
        text = self.screen.engine.database.language.texts['gui']['item_information']['name'] + item.name
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['name'] = {}
        self.texts['name']['text'] = text
        self.texts['name']['render'] = text_render
        self.texts['name']['position'] = starting_position

        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+25)
        text = self.screen.engine.database.language.texts['gui']['item_information']['type'] + self.screen.engine.database.language.texts['items']['type'][item.type]
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['type'] = {}
        self.texts['type']['text'] = text
        self.texts['type']['render'] = text_render
        self.texts['type']['position'] = starting_position

        space = 0
        if isinstance(item, items.Weapon):
            space = 75
            self.create_text_for_weapon(item)
        elif isinstance(item, items.Potion):
            space = 25
            self.create_text_for_potion(item)
        elif isinstance(item, items.BodyArmor):
            space = 25
            self.create_text_for_armor(item)

        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+50+space)
        text = self.screen.engine.database.language.texts['gui']['item_information']['weight'] + str(item.weight)
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['weight'] = {}
        self.texts['weight']['text'] = text
        self.texts['weight']['render'] = text_render
        self.texts['weight']['position'] = starting_position

        if self.where_is_item == 'inventory':
            stack = self.screen.engine.return_player().equipment.return_stack(item.id)
            if stack != None:
                all_weight = len(stack) * item.weight
                starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1] + 75 + space)
                text = self.screen.engine.database.language.texts['gui']['item_information']['all_weight']\
                       + str(len(stack)) + '*' + str(item.weight) + '=' + str(round(all_weight, 2))
                text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                      (0, 0, 0))
                self.texts['all_weight'] = {}
                self.texts['all_weight']['text'] = text
                self.texts['all_weight']['render'] = text_render
                self.texts['all_weight']['position'] = starting_position
                space += 25

                value = len(stack) * item.value
                starting_position = (
                    self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1] + 75 + space)
                text = self.screen.engine.database.language.texts['gui']['item_information']['value'] + str(value)
                text_render = self.screen.font.render(text,
                                                      int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                      (0, 0, 0))
        else:
            starting_position = (
            self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1] + 75 + space)
            text = self.screen.engine.database.language.texts['gui']['item_information']['value'] + str(item.value)
            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  (0, 0, 0))
        self.texts['value'] = {}
        self.texts['value']['text'] = text
        self.texts['value']['render'] = text_render
        self.texts['value']['position'] = starting_position

        starting_position = (
        self.sprites['free_square']['position'][0], self.sprites['free_square']['position'][1] + 300)
        text = item.description
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                              (0, 0, 0))
        self.texts['description'] = {}
        self.texts['description']['text'] = text
        self.texts['description']['render'] = text_render
        self.texts['description']['position'] = starting_position

        try:
            requirements = item.requirements
            player = self.screen.engine.return_player()
            red = (150, 0, 0)
            green = (0, 150, 0)

            starting_position = (
                self.sprites['free_square']['position'][0] + 510,
                self.sprites['free_square']['position'][1])
            text = self.screen.engine.database.language.texts['gui']['item_information']['requirements']
            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  (0, 0, 0))
            self.texts['requirements'] = {}
            self.texts['requirements']['text'] = text
            self.texts['requirements']['render'] = text_render
            self.texts['requirements']['position'] = starting_position

            starting_position = (
                self.sprites['free_square']['position'][0] + 510,
                self.sprites['free_square']['position'][1] + 25)
            text = self.screen.engine.database.language.texts['gui']['item_information']['level'] + str(requirements['level'])

            if requirements['level'] > player.statistics.level:
                color = red
            else:
                color = green

            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  color)
            self.texts['level'] = {}
            self.texts['level']['text'] = text
            self.texts['level']['render'] = text_render
            self.texts['level']['position'] = starting_position

            starting_position = (
                self.sprites['free_square']['position'][0] + 510,
                self.sprites['free_square']['position'][1] + 50)
            text = self.screen.engine.database.language.texts['gui']['item_information']['strength'] + str(requirements['strength'])

            if requirements['strength'] > player.statistics.strength:
                color = red
            else:
                color = green

            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  color)
            self.texts['strength'] = {}
            self.texts['strength']['text'] = text
            self.texts['strength']['render'] = text_render
            self.texts['strength']['position'] = starting_position

            starting_position = (
                self.sprites['free_square']['position'][0] + 510,
                self.sprites['free_square']['position'][1] + 75)
            text = self.screen.engine.database.language.texts['gui']['item_information']['agility'] + str(requirements['agility'])

            if requirements['agility'] > player.statistics.agility:
                color = red
            else:
                color = green

            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  color)
            self.texts['agility'] = {}
            self.texts['agility']['text'] = text
            self.texts['agility']['render'] = text_render
            self.texts['agility']['position'] = starting_position

            starting_position = (
                self.sprites['free_square']['position'][0] + 510,
                self.sprites['free_square']['position'][1] + 100)
            text = self.screen.engine.database.language.texts['gui']['item_information']['observation'] + str(requirements['observation'])

            if requirements['observation'] > player.statistics.observation:
                color = red
            else:
                color = green

            text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                  color)
            self.texts['observation'] = {}
            self.texts['observation']['text'] = text
            self.texts['observation']['render'] = text_render
            self.texts['observation']['position'] = starting_position
        except AttributeError:
            pass

    def create_text_for_weapon(self, item):
        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1] + 50)
        if item.one_handed:
            text = self.screen.engine.database.language.texts['gui']['item_information']['one_handed']
        else:
            text = self.screen.engine.database.language.texts['gui']['item_information']['two_handed']
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['one_handed'] = {}
        self.texts['one_handed']['text'] = text
        self.texts['one_handed']['render'] = text_render
        self.texts['one_handed']['position'] = starting_position

        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+75)
        text = self.screen.engine.database.language.texts['gui']['item_information']['damage']\
               + str(item.min_damage) + ' - ' + str(item.max_damage)
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['damage'] = {}
        self.texts['damage']['text'] = text
        self.texts['damage']['render'] = text_render
        self.texts['damage']['position'] = starting_position

        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+100)
        text = self.screen.engine.database.language.texts['gui']['item_information']['range'] + str(item.range)
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['range'] = {}
        self.texts['range']['text'] = text
        self.texts['range']['render'] = text_render
        self.texts['range']['position'] = starting_position

    def create_text_for_potion(self, item):
        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+50)
        text = self.screen.engine.database.language.texts['gui']['item_information']['numbers_of_turns'] + str(item.modifier.turns_to_end)
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['numbers_of_turns'] = {}
        self.texts['numbers_of_turns']['text'] = text
        self.texts['numbers_of_turns']['render'] = text_render
        self.texts['numbers_of_turns']['position'] = starting_position

        starting_position = (self.sprites['free_square']['position'][0] + 510, self.sprites['free_square']['position'][1])
        text = self.screen.engine.database.language.texts['gui']['item_information']['modifiers']
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['modifiers'] = {}
        self.texts['modifiers']['text'] = text
        self.texts['modifiers']['render'] = text_render
        self.texts['modifiers']['position'] = starting_position

        space = 25
        for effect in item.modifier.effects:
            if item.modifier.effects[effect]:
                starting_position = (self.sprites['free_square']['position'][0] + 510, self.sprites['free_square']['position'][1]+space)
                text = self.screen.engine.database.language.texts['gui']['item_information'][effect] + str(item.modifier.effects[effect])
                text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                         (0, 0, 0))
                self.texts[effect] = {}
                self.texts[effect]['text'] = text
                self.texts[effect]['render'] = text_render
                self.texts[effect]['position'] = starting_position
                space += 25

    def create_text_for_armor(self, item):
        starting_position = (self.sprites['free_square']['position'][0] + 210, self.sprites['free_square']['position'][1]+50)
        text = self.screen.engine.database.language.texts['gui']['item_information']['armor'] + str(item.armor)
        text_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']),
                                                 (0, 0, 0))
        self.texts['armor'] = {}
        self.texts['armor']['text'] = text
        self.texts['armor']['render'] = text_render
        self.texts['armor']['position'] = starting_position

    def render(self):
        for sprite in self.sprites:
            position = (self.sprites[sprite]['position'][0]
                        * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                        self.sprites[sprite]['position'][1]
                        * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
            self.screen.screen.blit(self.sprites[sprite]['sprite'], position)

        for button in self.buttons:
            self.buttons[button].render_button()

        for key in self.texts:
            position = (self.texts[key]['position'][0]
                        * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                        self.texts[key]['position'][1]
                        * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
            self.screen.screen.blit(self.texts[key]['render'], position)

    def load_item_portrait(self):

        self.sprites['free_square'] = {}
        self.sprites['free_square']['sprite'] = pygame.image.load(self.screen.engine.path + '/data/graphic/resources/free_item_square_big.png')
        self.sprites['free_square']['position'] = (self.position[0] + 25, self.position[1] + 50)

        text = self.screen.game.drawer.gui['item_information']['item'].image
        new_text = ''
        for letter in text:
            if letter == '.':
                break
            new_text += letter
        new_text += '_big.png'

        self.sprites['item'] = {}
        self.sprites['item']['sprite'] = pygame.image.load(self.screen.engine.path + '/data/graphic/items/' + new_text)
        self.sprites['item']['position'] = (self.position[0] + 33, self.position[1] + 58)

    def load_label_and_body(self):
        self.sprites['label'] = {}
        self.sprites['label']['sprite'] = pygame.image.load(
            self.screen.engine.path + '/data/graphic/gui/information/label.png')
        self.sprites['label']['position'] = (self.position[0], self.position[1])

        self.sprites['body'] = {}
        self.sprites['body']['sprite'] = pygame.image.load(
            self.screen.engine.path + '/data/graphic/gui/information/body.png')

        image_size = self.sprites['body']['sprite'].get_size()
        self.sprites['body']['position'] = (self.position[0], self.position[1]+40, image_size[0], image_size[1])

    def exit_button(self):
        if self.where_is_item == 'inventory':
            self.screen.game.gui['inventory'] = True
            if self.screen.game.drawer.gui['player']['inventory'] != None:
                self.screen.game.drawer.gui['player']['inventory'].render()
            if self.possibility == 1:
                self.screen.game.gui['container'] = True
                if self.screen.game.drawer.gui['container']['graphic_object'] != None:
                    self.screen.game.drawer.gui['container']['graphic_object'].render()

        if self.where_is_item == 'container':
            self.screen.game.gui['container'] = True
            if self.screen.game.drawer.gui['container']['graphic_object'] != None:
                self.screen.game.drawer.gui['container']['graphic_object'].render()
            if self.possibility == 2:
                self.screen.game.gui['inventory'] = True
                if self.screen.game.drawer.gui['player']['inventory'] != None:
                    self.screen.game.drawer.gui['player']['inventory'].render()

        self.screen.game.gui['item_information'] = False
        self.screen.game.drawer.gui['item_information']['item'] = None
        self.screen.game.drawer.gui['item_information']['graphic_object'] = None

    def clicked(self, mouse):
        if mouse[1][0]:
            for button in self.buttons:
                if self.buttons[button].is_clicked(mouse):
                    self.buttons[button].on_click()
                    return True
        return False
