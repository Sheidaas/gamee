import pygame
from data.modules.graphic.two_D import button


class Inventory:

    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory
        self.buttons = []
        self.sprites = {}
        self.item_sprites = {}
        self.dressed_item_sprites = {}
        self.texts = {}
        self.position = [460, 50]
        self.item_pages = {
            'current_page': 1,
            'all_pages': 1,
        }

    def render_text(self):
        for key in self.texts:
            self.screen.screen.blit(self.texts[key]['render'], self.texts[key]['position'])

    def render_item_sprites(self):

        position = [(self.position[0] + 290) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    (self.position[1] + 155) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1]]

        page = self.item_pages['current_page']
        for item in range(self.item_pages[page]['min'], self.item_pages[page]['max']):
            self.screen.screen.blit(self.sprites['free_square']['sprite'], position)
            item_position = [position[0] + (5 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]),
                             position[1] + (5 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])]
            try:
                self.screen.screen.blit(self.item_sprites[item]['sprite'], item_position)
                self.item_sprites[item]['position'] = item_position
            except KeyError:
                pass

            size = self.sprites['free_square']['sprite'].get_size()
            if position[0] + size[0] >\
                            ((self.position[0] + self.sprites['body']['size'][0])
                            * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]) - size[0]:
                position = ((self.position[0] + 290) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                            position[1] + (75 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1]))

            else:
                position = (position[0] + (75 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]),
                            position[1])

        for item in self.dressed_item_sprites:
            try:
                position = ((5 + self.sprites[item]['position'][0]) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                            (5 + self.sprites[item]['position'][1]) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0])
                self.dressed_item_sprites[item]['position'] = position
                self.screen.screen.blit(self.dressed_item_sprites[item]['sprite'], position)
            except KeyError:
                pass

    def render_sprites(self):
        for key in self.sprites:
            position = (self.sprites[key]['position'][0] * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                        self.sprites[key]['position'][1] * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
            self.screen.screen.blit(self.sprites[key]['sprite'], position)

    def create(self, screen, item_db):
        # Create label
        self.sprites['label'] = {}
        self.sprites['label']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/inventory/label.png')
        self.sprites['label']['size'] = (1000, 40)
        self.sprites['label']['position'] = self.position
        #

        # Create body
        self.sprites['body'] = {}
        self.sprites['body']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/inventory/body.png')
        self.sprites['body']['size'] = (1000, 760)
        self.sprites['body']['position'] = (self.position[0], self.position[1]+40)
        #

        # Create character
        self.sprites['character'] = {}
        self.sprites['character']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/inventory/character.png')
        self.sprites['character']['size'] = (240, 100)
        self.sprites['character']['position'] = (self.position[0]+250, self.position[1]+40)
        #

        # Create statistics
        self.sprites['statistics'] = {}
        self.sprites['statistics']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/inventory/statistics.png')
        self.sprites['statistics']['size'] = (240, 100)
        self.sprites['statistics']['position'] = (self.position[0]+495,  self.position[1]+40)
        #

        # Create inventory
        self.sprites['inventory'] = {}
        self.sprites['inventory']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/inventory/inventory.png')
        self.sprites['inventory']['size'] = (240, 100)
        self.sprites['inventory']['position'] = (self.position[0]+740,  self.position[1]+40)
        #

        # Create dressed armors squares

        self.sprites['free_square'] = {}
        self.sprites['free_square']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/resources/free_item_square.png')
        self.sprites['free_square']['size'] = (75, 75)
        self.sprites['free_square']['position'] = (-705, -705)

        # modulator
        self.sprites['modulator'] = {}
        self.sprites['modulator']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['modulator']['size'] = self.sprites['free_square']['size']
        self.sprites['modulator']['position'] = (self.position[0] + 10, self.position[1] + 50)

        # helmet
        self.sprites['helmet'] = {}
        self.sprites['helmet']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['helmet']['size'] = self.sprites['free_square']['size']
        self.sprites['helmet']['position'] = (self.position[0] + 90, self.position[1] + 50)

        # right_hand
        self.sprites['right-hand'] = {}
        self.sprites['right-hand']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['right-hand']['size'] = self.sprites['free_square']['size']
        self.sprites['right-hand']['position'] = (self.position[0] + 10, self.position[1] + 130)

        # armor
        self.sprites['armor'] = {}
        self.sprites['armor']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['armor']['size'] = self.sprites['free_square']['size']
        self.sprites['armor']['position'] = (self.position[0] + 90, self.position[1] + 130)

        # gloves
        self.sprites['gloves'] = {}
        self.sprites['gloves']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['gloves']['size'] = self.sprites['free_square']['size']
        self.sprites['gloves']['position'] = (self.position[0] + 170, self.position[1] + 130)

        # left_hand
        self.sprites['left-hand'] = {}
        self.sprites['left-hand']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['left-hand']['size'] = self.sprites['free_square']['size']
        self.sprites['left-hand']['position'] = (self.position[0] + 10, self.position[1] + 210)

        # leggings
        self.sprites['leggings'] = {}
        self.sprites['leggings']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['leggings']['size'] = self.sprites['free_square']['size']
        self.sprites['leggings']['position'] = (self.position[0] + 90, self.position[1] + 210)

        # boots
        self.sprites['boots'] = {}
        self.sprites['boots']['sprite'] = self.sprites['free_square']['sprite']
        self.sprites['boots']['size'] = self.sprites['free_square']['size']
        self.sprites['boots']['position'] = (self.position[0] + 90, self.position[1] + 290)

        # Create exit button
        self.buttons.append(button.Button(self.position[0] + 965,
                                          self.position[1] + 5,
                                          30, 30, 'x',screen.font, self.close_inventory,
                                          screen.screen, screen.engine.settings.graphic['screen'], screen))
        #

        #Create arrows buttons
        text = str(self.item_pages['current_page']) + '/' + str(self.item_pages['all_pages'])
        text_size = self.screen.font.size(text)
        image_size = (1255, 40)
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1] + 760

        self.buttons.append(button.Button(x - 45,
                                          y - 5,
                                          30, 30, '<',screen.font, self.page_button,
                                          screen.screen, screen.engine.settings.graphic['screen'], '<'))

        self.buttons.append(button.Button(x + 45,
                                          y - 5,
                                          30, 30, '>',screen.font, self.page_button,
                                          screen.screen, screen.engine.settings.graphic['screen'], '>'))

        #

        # Loading items images
        i = 0
        for item_stack in self.inventory.inventory:
            self.item_sprites[i] = {}
            self.item_sprites[i]['sprite'] = pygame.image.load(
                screen.engine.path + '/data/graphic/items/' + item_stack.item.image)
            i += 1


        for item in self.inventory.dressed_armor:
            if self.inventory.dressed_armor[item] != None:
                self.dressed_item_sprites[item] = {}
                self.dressed_item_sprites[item]['sprite'] = pygame.image.load(
                    screen.engine.path + '/data/graphic/items/' + self.inventory.dressed_armor[item].image)
        #

        pages = len(self.item_sprites) / 72 + 1
        for page in range(1, int(pages)+1):
            min = 1 * (72 * (page - 1))
            max = 72 * page
            self.item_pages[page] = {
                'min': min,
                'max': max,
            }
            self.item_pages['all_pages'] = page

        # Creating texts
        self.create_text()
        #

    def create_text(self):
        # Creating container title
        text = self.screen.engine.database.language.texts['gui']['inventory']['title']
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

        # Create page info
        text = str(self.item_pages['current_page']) + '/' + str(self.item_pages['all_pages'])
        text_size = self.screen.font.size(text)
        image_size = (1255, 40)
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1] + 760

        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['page'] = {}
        self.texts['page']['text'] = text
        self.texts['page']['render'] = text_to_render
        self.texts['page']['position'] = (x, y)

        # Create statistics info

        # Weight
        text = self.screen.engine.database.language.texts['gui']['inventory']['weight']\
               + str(round(self.inventory.equipment_weight, 3)) + '/' + str(self.inventory.equipment_max_weight)
        text_size = self.screen.font.size(text)
        image_size = (255, 40)
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1] + 400

        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['weight'] = {}
        self.texts['weight']['text'] = text
        self.texts['weight']['render'] = text_to_render
        self.texts['weight']['position'] = (x, y)
        #

        # Damage
        text = self.screen.engine.database.language.texts['gui']['inventory']['damage']\
               + str(self.inventory.statistics.min_damage) + ' - ' + str(self.inventory.statistics.max_damage)
        text_size = self.screen.font.size(text)
        image_size = (255, 40)
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1] + 430

        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['damage'] = {}
        self.texts['damage']['text'] = text
        self.texts['damage']['render'] = text_to_render
        self.texts['damage']['position'] = (x, y)
        #

        # Armor
        text = self.screen.engine.database.language.texts['gui']['inventory']['armor'] \
                + str(self.inventory.statistics.armor)
        text_size = self.screen.font.size(text)
        image_size = (255, 40)
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.position[0]
        y += self.position[1] + 460

        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(text, int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['armor'] = {}
        self.texts['armor']['text'] = text
        self.texts['armor']['render'] = text_to_render
        self.texts['armor']['position'] = (x, y)
        #

    def render(self):
        self.check_images_size()
        self.render_sprites()
        self.render_item_sprites()
        self.render_text()

        for button in self.buttons:
            button.render_button()

    def page_button(self, char):
        if char == '<':
            if self.item_pages['current_page'] > 1:
                self.item_pages['current_page'] -= 1
        else:
            if self.item_pages['current_page'] < self.item_pages['all_pages']:
                self.item_pages['current_page'] += 1

    def check_images_size(self):
        from data.modules.graphic.image_modificator import resize_image
        for key in self.sprites:
            self.sprites[key]['sprite'] = resize_image(self.screen, self.sprites[key]['sprite'])

        for key in self.item_sprites:
            self.item_sprites[key]['sprite'] = resize_image(self.screen, self.item_sprites[key]['sprite'])

        for key in self.dressed_item_sprites:
            self.dressed_item_sprites[key]['sprite'] = resize_image(self.screen, self.dressed_item_sprites[key]['sprite'])

    def open_statistics(self):
        self.screen.game.gui['statistics'] = True
        self.screen.game.gui['inventory'] = False

    def open_character(self):
        self.screen.game.gui['character'] = True
        self.screen.game.gui['inventory'] = False

    @staticmethod
    def close_inventory(screen):
        screen.game.gui['inventory'] = False
        screen.game.gui['character'] = False
        screen.game.gui['statistics'] = False
        screen.game.drawer.gui['inventory'] = None
        screen.game.drawer.gui['character'] = None
        screen.game.drawer.gui['statistics'] = None
