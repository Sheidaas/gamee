class Move:

    def move_to_force_direction(self, force_strength, force_destination, object_sprite, object):
        force = self.calculate_how_far_object_move(force_strength, object.mass)
        object_sprite.big_position = (object_sprite.big_position[0] + (force * force_destination[0]), object_sprite.big_position[1] + (force * force_destination[1]) )

    def calculate_how_far_object_move(self, force_strength, object_mass):
        return force_strength * object_mass
