class Interact:

    def __init__(self, persons_list: list):
        self.id = 0
        self.persons_list = persons_list
        self.name = ''

    def interact(self):
        pass


class Talk(Interact):

    def __init__(self, persons_list: list):
        self.id = 1
        self.name = 'talk'

    def interact(self):
        pass
