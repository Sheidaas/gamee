from data.modules.primary.statistics import Statistics
from data.modules.primary.abilities import Abilities
from data.modules.primary.equipments import Equipment
from data.modules.graphic.geometric_calculator import Calculator
from data.modules.primary.persons_move import Move


class Person:

    def __init__(self):
        self.id = 0
        self.map_sprite = ''
        self.portrait = ''
        self.name = ''
        self.last_name = ''
        self.age = ''
        self.mass = 50
        self.gender = ''
        self.race = None
        self.location = ''
        self.coordinate = [0, 0]  # x, y

        self.statistics = Statistics()
        self.abilities = Abilities(self.statistics)
        self.equipment = Equipment(self.statistics)

        self.ai = False

        # DONT SAVE THAT VARIABLES IN GAME_STATES
        self.visible_game_objects = {
            'visible_squares': [],  # square coordinate
            'visible_persons': [],  # person id
            'visible_objects': []   # objects id

        }

        self.visible_squares = []

    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.last_name

    def look_around(self, map_size: tuple) -> None:
        """

        This method is getting visible squares to this person

        Calculator() : objects have methods for calculating other objects
                       visible squares

        """
        self.visible_squares = Calculator().return_visible_positions(self, map_size)

    def set_race(self, race):
        self.race = race
        self.race.add_modifier_to_statistics(self.statistics)

    def return_abilities_id_to_list(self):
        return [ ability.id for ability in self.abilities.abilities ]

    def use_ability(self, id):
        self.abilities.use_ability(id)

    def uptade_coordinate(self, coordinate):
        self.coordinate = coordinate
