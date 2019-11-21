from .primary import maps
import sys


class GameStateLoader:

    def load_state(self, file_name, game_engine):
        game_engine.database.load_state(game_engine.path + '/saves/' + file_name + '/data/persons.json')
        game_engine.map = maps.MapLoader(game_engine.path, game_engine.path + '/saves' + file_name + '/data/maps/'
                                         + game_engine.return_player().location + '/map.json').return_map\
            (game_engine.database.person_database, game_engine.database.item_database, game_engine.loaded_game_resources)


class GameStateSaver:

    def save_state(self, game_engine, game_state_name):
        import subprocess
        bash_command_create_main_folder = 'mkdir ' + game_state_name
        bash_command_create_data_folder = 'mkdir data'
        bash_command_create_maps_folder = 'mkdir maps'
        bash_command_create_map_name_folder = 'mkdir ' + game_engine.map.name

        process = subprocess.Popen(bash_command_create_main_folder, shell=True, cwd=game_engine.path + '/saves/')
        process = subprocess.Popen(bash_command_create_data_folder, shell=True, cwd=game_engine.path + '/saves/' + game_state_name + '/')
        process = subprocess.Popen(bash_command_create_maps_folder, shell=True, cwd=game_engine.path + '/saves/' + game_state_name + '/data/')
        process = subprocess.Popen(bash_command_create_map_name_folder, shell=True, cwd=game_engine.path + '/saves/' + game_state_name + '/data/maps/')

        game_engine.database.person_database.save_persons_file(destination= game_engine.path + '/saves/' + game_state_name + '/data/persons.json')
        maps.MapSaver().save_map(game_engine.map, game_engine.path + '/saves/' + game_state_name + '/data/maps/' + game_engine.map.name + '/map.json')
