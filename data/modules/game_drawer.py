from .primary.player import Player
from .graphic.drawer_2d import Drawer
from .primary.turns_controller import TurnsController
from .primary.objects import Chest
from .graphic.two_D.player_gui.container import Containter
import pygame


class GameDrawer:

    def __init__(self, game_engine, screen):
        self.gui = {
            'main_menu': False,
            'menu': False,
            'settings': False,
            'settings_gui': False,
            'inventory': False,
            'character': False,
            'statistics': False,
            'container': False,
            'item_details': False,
            'person_detail': False,
            'object_detail': False,
            'item_information': False,
        }
        self.mouse = ( (), () )             # (mouse_pos_x, mouse_pos_y), (left_click, middle_click_, right_click)
        self.screen = screen
        self.game_engine = game_engine
        self.player_team_persons_id = [1]
        self.drawer = Drawer(screen)
        self.player_settings = Player( self.game_engine.return_player() )
        self.turns_controller = TurnsController()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    self.mouse = (self.mouse[0], ( pygame.mouse.get_pressed() ))
                    self.screen.mouse = self.mouse

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.gui['menu']:
                        self.gui['menu'] = False
                    else:
                        if self.gui['item_information']:
                            self.gui['item_information'] = False

                        elif self.gui['settings_gui']:
                            self.gui['settings_gui'] = False
                            self.gui['settings'] = True

                        elif self.gui['settings']:
                            self.gui['settings'] = False
                            self.gui['menu'] = True

                        elif self.gui['inventory']:
                            self.gui['inventory'] = False
                            self.drawer.gui['player']['inventory'] = None

                        else:
                            self.gui['menu'] = True

                for key in self.screen.engine.settings.primary_settings['key_layout']['interfaces'].keys():
                    if event.key == int(key):
                        if self.screen.engine.settings.primary_settings['key_layout']['interfaces'][key] == 'INVENTORY':
                            if self.gui['inventory']:
                                self.gui['inventory'] = False
                                self.drawer.gui['player']['inventory'] = None
                                self.gui['statistics'] = False
                                self.gui['character'] = False
                            else:
                                self.gui['inventory'] = True
                                self.gui['statistics'] = False
                                self.gui['character'] = False

                if event.key == pygame.K_1:
                    self.screen.engine.return_player().use_ability(1)

        keys = pygame.key.get_pressed()
        direction = [0, 0]
        for key in self.screen.engine.settings.primary_settings['key_layout']['move'].keys():
            if keys[int(key)]:
                if self.screen.engine.settings.primary_settings['key_layout']['move'][key] == 'FORWARD':
                    direction[1] -= 1
                elif self.screen.engine.settings.primary_settings['key_layout']['move'][key] == 'BACKWARD':
                    direction[1] += 1
                elif self.screen.engine.settings.primary_settings['key_layout']['move'][key] == 'TO_LEFT':
                    direction[0] -= 1
                else:
                    direction[0] += 1
            if direction:
                self.game_engine.move_person(direction, self.game_engine.return_player().id)

    def draw(self):
        self.drawer.camera.set_camera_to_follow_sprite(self.game_engine.loaded_game_resources.get_person_sprite_by_person_id(self.game_engine.return_player().id))
        if not self.gui['menu'] and not self.gui['settings_gui'] and not self.gui['settings']:
            self.drawer.render_terrain(self.screen, self.player_team_persons_id)
            self.drawer.render_objects(self.screen)
            self.drawer.render_persons(self.screen)

        self.drawer.render_gui(self.screen, self.gui)
        pygame.display.flip()

    def run(self):
        self.get_event()
        self.game_engine.pathfinder.setup_map_graph()
        self.game_engine.check_ai()
        self.check_objects_and_persons_positions()
        self.draw()
        self.where_is_mouse()
        self.drawer.camera.update_camera()

    def init(self):
        self.player_settings.load_player_saves_settings(self.game_engine.path, 'save_1')

    def check_objects_and_persons_positions(self):
        size = (75 * self.game_engine.settings.graphic['screen']['resolution_scale'][0],
                75 * self.game_engine.settings.graphic['screen']['resolution_scale'][1])

        for idx in self.game_engine.map.persons:
            person = self.game_engine.database.person_database.select_person_by_id(idx)
            person_sprite = self.game_engine.loaded_game_resources.get_person_sprite_by_person_id(idx)
            x = round(person_sprite.big_position[0] / size[0])
            y = round(person_sprite.big_position[1] / size[1])
            person.uptade_coordinate([x, y])
            person_sprite.small_position = (x, y)

    def where_is_mouse(self):
        gui_keys = ('health', 'location', 'coordinate', 'skills', 'minimap', 'experience')
        if self.mouse is not None:

            # checking if player clicked at gui
            for key in gui_keys:
                if self.drawer.gui['player']['hub'][key]:
                    if self.drawer.gui['player']['hub'][key].is_clicked(self.mouse):
                        if self.mouse[1][0] or self.mouse[1][1] or self.mouse[1][2]:
                            self.drawer.gui['player']['hub'][key].clicked(self.mouse)
                            self.mouse = None
                            return True

            # checking if player clicked at item information
            if self.gui['item_information']:
                if self.drawer.gui['item_information']['graphic_object'].clicked(self.mouse):
                    self.mouse = None
                    return True

            # checking if player clicked at item details
            if self.gui['item_details']:
                if self.mouse[1][0]:
                    if self.screen.game.drawer.gui['item_details']['graphic_object'].clicked(self.mouse):
                        self.mouse = None
                        return True

                    if self.drawer.gui['item_details']['graphic_object'].is_clicked_without_details(self.mouse[0]):
                        self.gui['item_details'] = False
                        self.mouse = None
                        return True

            # checking if player clicked at open container
            if self.gui['container']:
                if self.drawer.gui['container']['graphic_object'].is_clicked(self.mouse):
                    if self.mouse[1][0]:
                        self.drawer.gui['container']['graphic_object'].clicked(self.mouse)
                        self.mouse = None
                        return True

            # checking if player clicked at inventory
            if self.drawer.gui['player']['inventory']:
                if self.drawer.gui['player']['inventory'].is_clicked(self.mouse):
                    if self.mouse[1][0] or self.mouse[1][1] or self.mouse[1][2]:
                        self.drawer.gui['player']['inventory'].clicked(self.mouse)
                        self.mouse = None
                        return True

            # first checking if clicked at person
            for person in self.game_engine.loaded_game_resources.person_sprite_menager.sprites():
                if self.drawer.is_mouse_clicked_in_object_on_map(person, self.mouse[0]):
                    if self.mouse[1][0] or self.mouse[1][1] or self.mouse[1][2]:
                        print(person.person_id)
                        self.mouse = None
                        return True

            # second checking if clicked at object
            for _object in self.game_engine.loaded_game_resources.objects_sprite_menager.sprites():
                if self.drawer.is_mouse_clicked_in_object_on_map(_object, self.mouse[0]):
                    if self.mouse[1][0] or self.mouse[1][1] or self.mouse[1][2]:
                        _object = self.screen.engine.map.objects[str(_object.object_id)]
                        if type(_object['object']) == Chest:
                            self.gui['container'] = True
                            self.screen.game.drawer.gui['container']['container'] = _object['object']
                            self.screen.game.drawer.gui['container']['graphic_object'] = Containter(self.screen.game.drawer.gui['container']['container'], self.screen)
                            self.screen.game.drawer.gui['container']['graphic_object'].create(self.screen, self.screen.engine.database.item_database)
                            self.screen.game.drawer.gui['container']['graphic_object'].render()
                            self.mouse = None
                            return True
