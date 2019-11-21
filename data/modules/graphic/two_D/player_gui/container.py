import pygame
from data.modules.graphic.two_D import button


class Containter:

    def __init__(self, container, screen):
        self.screen = screen
        self.container = container
        self.buttons = []
        self.sprites = {
            'label': {

            },
            'body': {

            }
        }
        self.item_sprites = {}
        self.texts = {
            'title': {

            }
        }

    def create(self, screen, item_db):
        # Create label
        self.sprites['label']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/container/first.png')
        self.sprites['label']['size'] = (310, 40)
        #

        # Create body
        self.sprites['body']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/gui/container/second.png')
        self.sprites['body']['size'] = (310, 310)

        self.sprites['free_square'] = {}
        self.sprites['free_square']['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/resources/free_item_square.png')
        self.sprites['free_square']['size'] = (75, 75)
        self.sprites['free_square']['position'] = (-705, -705)

        # Create exit button
        self.buttons.append(button.Button(screen.game.drawer.gui['container']['last_position'][0] + 275,
                                          screen.game.drawer.gui['container']['last_position'][1] + 5,
                                          30, 30, 'x',screen.font, self.close_container,
                                          screen.screen, screen.engine.settings.graphic['screen'], screen))

        self.buttons.append(button.Button(screen.game.drawer.gui['container']['last_position'][0],
                                          screen.game.drawer.gui['container']['last_position'][1] + 350,
                                          310, 30, self.screen.engine.database.language.texts['gui']['container']['take_all'],
                                          screen.font, self.take_all_items,
                                          screen.screen, screen.engine.settings.graphic['screen'], screen))

        #

        # Loading items images
        i = 0
        for item in self.container.content:
            self.item_sprites[i] = {}
            self.item_sprites[i]['sprite'] = pygame.image.load(screen.engine.path + '/data/graphic/items/' + item.image)
            i += 1
        #

        # Creating texts
        self.create_text()
        #

    def create_text(self):
        # Creating container title
        text_size = self.screen.font.size(self.screen.engine.database.language.texts['gui']['container'][self.container.name])
        image_size = self.sprites['label']['sprite'].get_size()
        x = image_size[0] - text_size[0]
        y = image_size[1] - text_size[1]
        x /= 2
        y /= 2
        x += self.screen.game.drawer.gui['container']['last_position'][0]
        y += self.screen.game.drawer.gui['container']['last_position'][1]
        x *= self.screen.engine.settings.graphic['screen']['resolution_scale'][0]
        y *= self.screen.engine.settings.graphic['screen']['resolution_scale'][1]

        text_to_render = self.screen.font.render(self.screen.engine.database.language.texts['gui']['container'][self.container.name], int(self.screen.engine.settings.graphic['screen']['antialias']), (0, 0, 0))
        self.texts['title']['render'] = text_to_render
        self.texts['title']['position'] = (x, y)
        #

    def render_text(self):
        for key in self.texts:
            self.screen.screen.blit(self.texts[key]['render'], self.texts[key]['position'])

    def render(self):
        self.check_images_size()
        self.render_sprites()
        self.render_item_sprites()
        self.render_text()


        for button in self.buttons:
            button.render_button()

    def render_item_sprites(self):
        position = [(self.screen.game.drawer.gui['container']['last_position'][0]
                    + 5) * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                    (self.screen.game.drawer.gui['container']['last_position'][1] + 40)
                    * self.screen.engine.settings.graphic['screen']['resolution_scale'][1]]

        for item in self.item_sprites:
            self.screen.screen.blit(self.sprites['free_square']['sprite'], position)
            item_position = [position[0] + (5 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]),
                             position[1] + (5 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])]
            try:
                self.screen.screen.blit(self.item_sprites[item]['sprite'], item_position)
                self.item_sprites[item]['position'] = item_position
            except KeyError:
                pass

            size = self.sprites['free_square']['sprite'].get_size()
            if position[0] + size[0] > (310 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]):
                position = ((self.screen.game.drawer.gui['container']['last_position'][0] + 5)
                            * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                            position[1] + size[1])
            else:
                position = (position[0] + size[0], position[1])

    def render_sprites(self):
        self.sprites['label']['position'] = (self.screen.game.drawer.gui['container']['last_position'][0]
                                             * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                                             self.screen.game.drawer.gui['container']['last_position'][1]
                                             * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])

        self.sprites['body']['position'] = (self.screen.game.drawer.gui['container']['last_position'][0]
                                            * self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                                            (self.screen.game.drawer.gui['container']['last_position'][1]
                                            + 40) * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])

        for key in self.sprites:
            self.screen.screen.blit(self.sprites[key]['sprite'], self.sprites[key]['position'])

    def check_images_size(self):
        from data.modules.graphic.image_modificator import resize_image
        for key in self.sprites:
            self.sprites[key]['sprite'] = resize_image(self.screen, self.sprites[key]['sprite'])

        for key in self.item_sprites:
            self.item_sprites[key]['sprite'] = resize_image(self.screen, self.item_sprites[key]['sprite'])

    @staticmethod
    def close_container(screen):
        screen.game.gui['container'] = False
        screen.game.drawer.gui['container']['graphic_object'] = None
        screen.game.drawer.gui['container']['container'] = None

    def take_all_items(self, screen):
        if len(self.container.content) > 1:
            self.container.give_away_all_items(screen.engine.return_player())
            screen.game.drawer.gui['container']['graphic_object'] = None
            screen.game.drawer.gui['container']['graphic_object'] = Containter(screen.game.drawer.gui['container']['container'], screen)
            screen.game.drawer.gui['container']['graphic_object'].create(screen, screen.engine.database.item_database)
            screen.game.drawer.gui['container']['graphic_object'].render()

            if screen.game.gui['inventory']:
                screen.game.drawer.gui['player']['inventory'] = None
                from data.modules.graphic.two_D.player_gui import inventory
                screen.game.drawer.gui['player']['inventory'] = inventory.Inventory(screen, screen.engine.return_player().equipment)
                screen.game.drawer.gui['player']['inventory'].create(screen, screen.engine.database.item_database)
                screen.game.drawer.gui['player']['inventory'].render()
