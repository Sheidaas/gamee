from data.modules.graphic.geometric_calculator import Calculator
from copy import deepcopy


class PersonArtificialIntelligence:

    def __init__(self, person):
        self.level = 0
        self.person = person

        self.current_goal = ''
        self.current_action = ''

        self.goals = {
            'go_to_destination': ('move', 10),
            'attack': ('attack', 0),
            'stay_in_position': ('stay', 9),
        }
        self.actions = {
            'move': {
                'start_position': self.get_start_position,
                'destination_position': (),
                'path': [],
                'function': self.go_to
            }
        }
        self.memory = {
            'last_start_position': (),
            'last_destination_position': (),
            'last_path': [],
        }

        self.terrain_calculator = Calculator()

    def go_to(self, destination_position, game_engine):
        self.actions['move']['destination_position'] = destination_position
        if self.memory['last_path']:
            if len(self.memory['last_path']) > 1:

                if not self.memory['last_path'][1].can_walk and\
                        self.memory['last_destination_position'] != destination_position:
                    new_path = self.get_new_path(game_engine)
                    self.walk_through_path(game_engine, new_path)
                    return True
                else:
                    self.walk_through_path(game_engine, self.memory['last_path'])
                    return True

            if not self.should_continue_path() and self.memory['last_destination_position'] != destination_position:
                new_path = self.get_new_path(game_engine)
                self.walk_through_path(game_engine, new_path)
                return True
            else:
                new_path = self.get_extended_path(self.memory['last_path'][-1].coordinate,
                                                  self.actions['move']['destination_position'], game_engine)

                # check if exist path to destination
                # if new path is not false, then append extended path to
                if new_path:
                    self.memory['last_path'] += new_path
                    self.walk_through_path(game_engine, self.memory['last_path'])
                    return True
                else:
                    new_path = self.get_new_path(game_engine)
                    self.walk_through_path(game_engine, new_path)
                    return True
        else:
            new_path = self.get_new_path(game_engine)
            self.walk_through_path(game_engine, new_path)

    def get_start_position(self):
        return tuple(self.person.coordinate)

    def get_decision(self, game_engine):
        largest_goal_value = 0.0
        goal_key = ''
        for goal in self.goals:
            if self.goals[goal][1] > largest_goal_value:
                largest_goal_value = self.goals[goal][1]
                goal_key = self.goals[goal][0]
        self.actions[goal_key]['function'](game_engine.return_player().coordinate, game_engine)

    def walk_through_path(self, game_engine, path):
        person_sprite = game_engine.loaded_game_resources.get_person_sprite_by_person_id(self.person.id)
        if path and person_sprite:
            if len(path) > 1 and path[1].can_walk:
                if person_sprite.big_position[0] > path[1].big_position[1]:
                    x = -1
                elif person_sprite.big_position[0] < path[1].big_position[1]:
                    x = 1
                else:
                    x = 0
                if person_sprite.big_position[1] > path[1].big_position[0]:
                    y = -1
                elif person_sprite.big_position[1] < path[1].big_position[0]:
                    y = 1
                else:
                    y = 0
                game_engine.move_person([x, y], self.person.id)
                if self.actions['move']['start_position']() == (path[1].coordinate[1], path[1].coordinate[0]):  # path.coordinate is [y, x]
                    if path[0] in self.memory['last_path']:
                        self.memory['last_path'].remove(path[0])

    def get_new_path(self, game_engine):
        new_path = game_engine.pathfinder.return_path(self.actions['move']['start_position'](), self.actions['move']['destination_position'])
        self.memory['last_start_position'] = self.actions['move']['start_position']()
        self.memory['last_destination_position'] = self.actions['move']['destination_position']
        self.memory['last_path'] = deepcopy(new_path)

        if new_path:
            game_engine.pathfinder.map_graph[new_path[0].coordinate[1]][
                new_path[0].coordinate[0]].can_walk = False

            game_engine.pathfinder.map_graph[new_path[-1].coordinate[1]][
                new_path[-1].coordinate[0]].can_walk = False

        return new_path

    def get_extended_path(self, start_position: tuple, destination_position: tuple, game_engine):
        new_path = game_engine.pathfinder.return_path(start_position, destination_position)
        self.memory['last_start_position'] = self.actions['move']['start_position']()
        self.memory['last_destination_position'] = self.actions['move']['destination_position']
        if len(new_path) > 1:
            new_path.pop(0)
        if new_path:
            game_engine.pathfinder.map_graph[new_path[0].coordinate[1]][
                new_path[0].coordinate[0]].can_walk = True

            game_engine.pathfinder.map_graph[new_path[-1].coordinate[1]][
                new_path[-1].coordinate[0]].can_walk = False

            game_engine.pathfinder.map_graph[self.memory['last_start_position'][0]][
                self.memory['last_start_position'][1]].can_walk = False
        return new_path

    def add_path_to_last_path(self, path):
        self.memory['last_path'] += deepcopy(path)

    def should_continue_path(self):
        return self.terrain_calculator.is_object_in_area(self.actions['move']['destination_position'],
                                                         self.memory['last_path'][-1].coordinate, 5)
