from data.modules.primary import persons


class Enemy(persons.Person):
    def __init__(self):
        super().__init__()
        self.giving_experience = 0

