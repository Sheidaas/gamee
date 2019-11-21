import json


class Player:
    def __init__(self, person):
        self.person = person
        self.key_layout = {}

    def load_player_saves_settings(self, game_path, save_name):
        path = game_path + '/saves/' + save_name + '/player_settings.json'
        try:
            with open(path, 'r') as file:
                data = file.read()
                self.set_player_saves_settings(json.loads(data))
        except FileExistsError:
            print('key_layout file exists error #PATH: ' + path)

    def set_player_saves_settings(self, player_saves_settings):
        self.key_layout = player_saves_settings['key_layout']

