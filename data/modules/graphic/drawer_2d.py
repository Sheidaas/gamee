import pygame
from data.modules.graphic.geometric_calculator import Calculator
from data.modules.graphic.two_D.menu import Menu
from data.modules.graphic.two_D.settings import Settings
from data.modules.graphic.two_D.settings_player_gui import Settings as SettingsPlayerGui
from data.modules.graphic.two_D.player_gui import health, bottom_panel, location, experience, grid, container, inventory, item_details
from data.modules.graphic.sprites.person import PersonSprite
from data.modules.camera import Camera


class Drawer:

    def __init__(self, screen):
        self.gui = {
            'player': {
                'hub': {
                    'health': None,
                    'location': None,
                    'coordinate': None,
                    'skills': None,
                    'grid': None,
                    'minimap': None,
                    'experience': None,
                },
                'inventory': None,
                'character': None,
                'statistics': None,
            },
            'item_details': {
                'item': None,
                'graphic_object': None,
            },
            'person_detail': {
                'person': None,
                'graphic_object': None,
            },
            'object_detail': {
                'object': None,
                'graphic_object': None,
            },
            'item_information': {
                'item': None,
                'graphic_object': None
            },
            'main_menu': None,
            'menu': None,
            'settings': None,
            'settings_gui': None,
            'container': {
                'graphic_object': None,
                'container': None,
                'last_position': (50, 300)
            },
        }
        self.geometric_calculator = Calculator()
        self.last_player_position = []
        self.visible_squares = []                                                # squares visibles by player
        self.positions_square = []
        self.center_view = (550, 300)                                  # squares vertex in pixels
        self.square_size_in_pixel = (0, 0)
        self.camera = Camera((screen.engine.settings.graphic['screen']['resolution_x'],
                              screen.engine.settings.graphic['screen']['resolution_y']),
                              (0, 0), [])

    def render_terrain(self, screen, persons_id: list):
        for person_id in persons_id:
            screen.engine.database.person_database.select_person_by_id(person_id).look_around(screen.engine.map.size)
            self.visible_squares = screen.engine.database.person_database.select_person_by_id(person_id).visible_squares

        for position in self.visible_squares:
            sprite = screen.engine.loaded_game_resources.get_terrain_sprite_by_small_position(position)
            screen.screen.blit(screen.engine.loaded_game_resources.get_terrain_image_by_id(sprite.image_id), self.return_render_position(sprite.big_position))

    def render_persons(self, screen):
        for person_id in screen.engine.map.persons:
            person = screen.engine.database.person_database.select_person_by_id(person_id)
            if tuple(person.coordinate) in self.visible_squares:
                sprite = screen.engine.loaded_game_resources.get_person_sprite_by_small_position(person.coordinate)
                screen.screen.blit(sprite.image, self.return_render_position(sprite.big_position))

    def render_objects(self, screen):
        for _object in screen.engine.map.objects:
            if tuple(screen.engine.map.objects[_object]['object'].coordinate) in self.visible_squares:
                sprite = screen.engine.loaded_game_resources.get_object_sprite_by_small_position(tuple(screen.engine.map.objects[_object]['object'].coordinate))
                screen.screen.blit(sprite.image, self.return_render_position(sprite.big_position))

                if screen.mouse[1][0]:
                    if self.is_mouse_clicked_in_object_on_map(sprite, screen.mouse[0]):
                        self.mouse_clicked_in_object(screen.engine.map.objects[_object]['object'], screen.engine.return_player(), screen)
                        screen.mouse = (None, (0, 0, 0))
                elif screen.mouse[1][1]:
                    if self.is_mouse_clicked_in_object_on_map(screen.engine.map.objects[_object]['object'], sprite.big_position, screen.mouse[0], 'right'):
                        pass

    def return_render_position(self, big_position, with_camera=True):
        if with_camera:
            return (big_position[0] - self.camera.position[0] + self.center_view[0], big_position[1] - self.camera.position[1] + self.center_view[1])
        return big_position

    def render_gui(self, screen, gui):
        if not gui['menu'] and not gui['settings'] and not gui['settings_gui']:
            if screen.engine.settings.graphic['screen']['player']['grid']:
                if self.gui['player']['hub']['grid'] is None:
                    self.gui['player']['hub']['grid'] = grid.Grid()
                    self.gui['player']['hub']['grid'].create(screen)
                else:
                    self.gui['player']['hub']['grid'].render(screen)

            if screen.engine.settings.graphic['screen']['player']['health']:
                if self.gui['player']['hub']['health'] is None:
                    self.gui['player']['hub']['health'] = health.Health(50, 50, screen.engine.return_player(), screen)
                    self.gui['player']['hub']['health'].create()
                else:
                    self.gui['player']['hub']['health'].render()

            if screen.engine.settings.graphic['screen']['player']['skills']:
                if self.gui['player']['hub']['skills'] is None:
                    self.gui['player']['hub']['skills'] = bottom_panel.BottomPanel(360, 955, screen.engine.return_player(), screen)
                    self.gui['player']['hub']['skills'].create()
                else:
                    self.gui['player']['hub']['skills'].render()

            if screen.engine.settings.graphic['screen']['player']['location']:
                if self.gui['player']['hub']['location'] is None:
                    self.gui['player']['hub']['location'] = location.Location(50, 130, screen.engine.return_player(), screen)
                    self.gui['player']['hub']['location'].create()
                else:
                    self.gui['player']['hub']['location'].render()

            if screen.engine.settings.graphic['screen']['player']['experience']:
                if self.gui['player']['hub']['experience'] is None:
                    self.gui['player']['hub']['experience'] = experience.Experience(360, 920, screen.engine.return_player(), screen, screen.engine.path)
                    self.gui['player']['hub']['experience'].create()
                else:
                    self.gui['player']['hub']['experience'].render()

            if gui['container']:
                if self.gui['container']['graphic_object'] is None:
                    self.gui['container']['graphic_object'] = container.Containter(self.gui['container']['container'], screen)
                    self.gui['container']['graphic_object'].create(screen, screen.engine.database.item_database)
                else:
                    self.gui['container']['graphic_object'].render()
                    if not self.geometric_calculator.is_object_in_area(self.gui['container']['container'].coordinate,
                                                                   screen.engine.return_player().coordinate):
                        gui['container'] = False
                        self.gui['container']['container'] = None
                        self.gui['container']['graphic_object'] = None

            if gui['inventory']:
                if self.gui['player']['inventory'] is None:
                    self.gui['player']['inventory'] = inventory.Inventory(screen, screen.engine.return_player().equipment)
                    self.gui['player']['inventory'].create(screen, screen.engine.database.item_database)
                else:
                    self.gui['player']['inventory'].render()

            if gui['item_details']:
                self.gui['item_details']['graphic_object'].create()
                self.gui['item_details']['graphic_object'].render()

            if gui['item_information']:
                self.gui['item_information']['graphic_object'].render()

        else:
            if gui['menu']:
                if self.gui['menu'] == None:
                    self.gui['menu'] = Menu()
                    self.gui['menu'].create(screen)
                    self.render(self.gui['menu'], screen)
                else:
                    self.render(self.gui['menu'], screen)
                    if screen.mouse[1][0]:
                        self.is_mouse_clicked('menu', screen.mouse[0])
                        screen.mouse = (None, (0,0,0))
            else:
                self.gui['menu'] = None

            if gui['settings']:
                if self.gui['settings'] == None:
                    self.gui['settings'] = Settings()
                    self.gui['settings'].create_buttons(screen)
                    self.render(self.gui['settings'], screen)
                else:
                    if self.gui['settings'].update:
                        self.gui['settings'].create_buttons(screen)
                    self.render(self.gui['settings'], screen)
                    if screen.mouse[1][0]:
                        self.is_mouse_clicked('settings', screen.mouse[0])
                        screen.mouse = (None, (0,0,0))
            else:
                self.gui['settings'] = None

            if gui['settings_gui']:
                if self.gui['settings_gui'] == None:
                    self.gui['settings_gui'] = SettingsPlayerGui()
                    self.gui['settings_gui'].create_buttons(screen)
                    self.render(self.gui['settings_gui'], screen)
                else:
                    if self.gui['settings_gui'].update:
                        self.gui['settings_gui'].create_buttons(screen)
                    self.render(self.gui['settings_gui'], screen)
                    if screen.mouse[1][0]:
                        self.is_mouse_clicked('settings_gui', screen.mouse[0])
                        screen.mouse = (None, (0,0,0))
            else:
                self.gui['settings_gui'] = None

    def render(self, obj, screen):
        self.render_background(obj)
        self.render_images(obj, screen)
        self.render_buttons(obj)

    @staticmethod
    def render_buttons(obj):
        for key in obj.buttons:
            obj.buttons[key].render_button()

    @staticmethod
    def render_background(obj):
        if obj.background != None:
            obj.background.render_background()

    @staticmethod
    def render_images(obj, screen):
        for image in obj.images:
            screen.screen.blit(obj.images[image][0], obj.images[image][1])

    @staticmethod
    def mouse_clicked_in_button(button):
        button.on_click()

    @staticmethod
    def is_mouse_clicked_in_button(button, mouse_position):
        area = (button.start[0], button.start[1], button.start[0] + button.size[0], button.start[1] + button.size[1])
        if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
            and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
            return True
        return False

    def is_mouse_clicked_in_object_on_map(self, sprite, mouse_position):
        try:
            img_size = sprite.image.get_size()
            image_position = self.return_render_position(sprite.big_position)
        except AttributeError:
            img_size = sprite['sprite'].get_size()
            image_position = self.return_render_position(sprite['position'], with_camera=False)
        finally:
            area = (image_position[0], image_position[1], image_position[0] + img_size[0], image_position[1] + img_size[1])
            if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
                and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
                return True
            return False

    def mouse_clicked_in_object(self, obj, player, screen):
        from data.modules.primary import objects
        if screen.game.gui['inventory'] is False and screen.game.gui['statistics'] is False and screen.game.gui['character'] is False:
            if self.geometric_calculator.is_object_in_area(obj.coordinate, screen.engine.return_player().coordinate):
                if isinstance(obj, objects.Chest):
                    screen.game.gui['container'] = True
                    self.gui['container']['container'] = obj

    def is_mouse_clicked(self, screen_key, mouse_pos):
        for key in self.gui[screen_key].buttons.keys():
            if self.is_mouse_clicked_in_button(self.gui[screen_key].buttons[key], mouse_pos):
                self.mouse_clicked_in_button(self.gui[screen_key].buttons[key])
                break
