from data.modules.primary import settings_loader
from data.modules.primary import database
from data.modules.game_loaded_resources_manager import LoadedResourcesMenager
from data.modules import game_state
from data.modules.primary.persons_move import Move
from data.modules.primary.pathfinder import Pathfinder
from data.modules.primary.artificial_intelligence import PersonArtificialIntelligence
import os


class GameEngine:

    def __init__(self, screen):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.settings = settings_loader.SettingsLoader(self.path, '/settings.ini').return_settings()
        self.database = database.Database(self.path, self.settings.primary_settings['language'])
        self.loaded_game_resources = LoadedResourcesMenager(screen)
        self.map = None
        self.pathfinder = None

    def init_engine(self):
        self.database.init_databases()

    def init_state(self, state_name, screen):
        game_state.GameStateLoader().load_state(state_name, self)
        self.pathfinder = Pathfinder(self.map, screen)

    def save_state(self, state_name):
        game_state.GameStateSaver().save_state(self, state_name)

    def save_settings(self):
        settings = {
            '1': self.settings.primary_settings,
            '2': self.settings.graphic
        }
        saver = settings_loader.SettingsLoader(self.path, '/settings.ini')
        saver.settings = settings
        saver.save_settings()

    def return_player(self):
        for player in self.database.person_database.persons:
            if player.id == 1:
                return player

    def next_turn(self):
        pass

    def move_person(self, direction, person_id):
        person = self.database.person_database.select_person_by_id(person_id)
        sprite = self.loaded_game_resources.get_person_sprite_by_person_id(person_id)

        Move().move_to_force_direction(0.05, direction, sprite, person)

    def check_ai(self):
        for person in self.database.person_database.persons:
            if person.ai:
                person.ai.get_decision(self)
                



