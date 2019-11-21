from data.modules.primary import itemdatabase
from data.modules.primary import abilities_classes
from data.modules.primary import persondatabase
from data.modules.primary.races import RaceDatabases
from data.modules.primary import language as lang


class Database:

    def __init__(self, path: str, language: str):
        self.language = lang.LanguageLoader(path, language).return_language()
        self.person_database = persondatabase.Database(path)
        self.item_database = itemdatabase.Database(path, self.language.texts['items'])
        self.races_database = RaceDatabases(path, self.language.texts['races'])
        self.abilities_database = abilities_classes.Database()
        self.maps_keys = ['starting_maps', ]

    def init_databases(self):
        self.item_database.init_database()
        self.races_database.init_database()
        self.abilities_database.init_database()
        self.person_database.init_database(self.races_database, self.item_database, self.abilities_database)

    def save_current_state(self, destination):
        self.person_database.save_persons_file(destination)

    def load_state(self, person_database_path):
        self.item_database.init_database()
        self.races_database.init_database()
        self.abilities_database.init_database()
        self.person_database.init_database(self.races_database, self.item_database, self.abilities_database, person_database_path)

    def save_state(self, screen, destination):
        person_database_path = destination + '/data/persons.json'
        self.person_database.save_persons_file(person_database_path)

        screen.engine.save_map(destination + '/data/maps/' + screen.engine.return_player().location)
