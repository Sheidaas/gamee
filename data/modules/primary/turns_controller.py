class TurnsController:

    def __init__(self):
        self.current_person_id_turn = 0
        self.current_person_action_points = 0
        self.current_person_time_to_end_turn = 0
        self.is_person_visible_to_player = True
        self.is_person_controlled_by_player = True

    def next_turn(self, person_database):
        for person in person_database.persons:
            if person.id == self.current_person_id_turn:
                person.statistics.modifiers.change_statistics()
                break
