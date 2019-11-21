import json

class LanguageLoader:

    def __init__(self, path: str, language: str):
        self.language = {}
        self.file_destination = path + '/data/languages/' + str(language)

    def load_language(self):
        files_to_load = [
            ('gui', '/gui_file.json'),
            ('items', '/items_file.json'),
            ('races', '/races_file.json'),
        ]

        for file_to_load in files_to_load:
            with open(self.file_destination + file_to_load[1], 'r') as file:
                data = file.read()
                self.language[file_to_load[0]] = json.loads(data)

    def return_language(self):
        self.load_language()
        language = Language()
        language.texts['gui'] = self.language['gui']
        language.texts['items'] = self.language['items']
        language.texts['races'] = self.language['races']
        return language


class Language:

    def __init__(self):
        self.texts = {}
