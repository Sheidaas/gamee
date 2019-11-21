import json


class SettingsLoader:

    def __init__(self, path, file_destination: str):
        self.settings = {}
        self.file_destination = path + file_destination

    def load_settings(self):
        with open(self.file_destination, 'r') as file:
            data = file.read()
            self.settings = json.loads(data)

    def save_settings(self):
        with open(self.file_destination, 'w') as file:
            file.write(json.dumps(self.settings, indent=4))

    def return_settings(self):
        self.load_settings()
        settings = Settings()
        settings.primary_settings = self.settings['1']
        settings.graphic = self.settings['2']
        return settings

class Settings:

    def __init__(self):
        self.graphic = {}
        self.primary_settings = {}
