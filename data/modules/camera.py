from copy import deepcopy


class Camera:

    def __init__(self, screen_resolution, square_size, positions_square, is_following=False, following_object=None):
        self.last_position = (0, 0, 0)          # X, Y, Z (x - horizontal, y - vertical, z - sprites scale)
        self.position = (0, 0, 0)               # X, Y, Z (x - horizontal, y - vertical, z - sprites scale)

        self.visible_space = ((0, 0), (0, 0))   # (x_min, x_max), (y_min, y_max)
        self.vertex_positions = {
                                                """
                                                    a
                                                x1_____x2
                                                |       |
                                                |       | b
                                                |       |
                                                y1------y2

                                                """
            'x1': tuple,
            'x2': tuple,
            'y1': tuple,
            'y2': tuple
        }
        self.screen_resolution = screen_resolution
        self.square_size = square_size
        self.positions_square = positions_square
        self.is_following = is_following
        self.following_object = following_object

        self.visible_persons = ()

    def update_camera(self):
        if self.is_following:
            self.follow_object()

        self.calculate_vertex_positions()
        self.calculate_visible_space()

    def is_position_changed(self):
        if self.last_position == self.position:
            return True
        return False

    def set_camera_to_follow_sprite(self, sprite):
        self.is_following = True
        self.following_object = sprite

    def follow_object(self):
        position_diffrence = (self.following_object.big_position[0] - self.position[0],  # X
                              self.following_object.big_position[1] - self.position[1])  # Y
        if position_diffrence != (0, 0):
            self.move_camera(position_diffrence)

    def move_camera(self, position: tuple):
        self.last_position = deepcopy(self.position)
        self.position = (self.position[0] + position[0],  # X
                         self.position[1] + position[1],  # Y
                         self.position[2])                # Z

    def move_camera_in_z_scale(self, _y):
        self.last_position = deepcopy(self.position)
        self.position = (self.position[0],       # X
                         self.position[1],       # Y
                         self.position[2] + _y)  # Z

    def calculate_vertex_positions(self):
        x1_x = self.position[0] + self.screen_resolution[0]
        x1_y = self.position[1] + self.screen_resolution[1]
        self.vertex_positions['x1'] = (x1_x, x1_y)

        x2_x = self.position[0] - self.screen_resolution[0]
        x2_y = self.position[1] - self.screen_resolution[1]

        self.vertex_positions['x2'] = (x2_x, x2_y)

        y1_x = self.position[0] + self.screen_resolution[0]
        y1_y = self.position[1] - self.screen_resolution[1]

        self.vertex_positions['y1'] = (y1_x, y1_y)

        y2_x = self.position[0] - self.screen_resolution[0]
        y2_y = self.position[1] + self.screen_resolution[1]

        self.vertex_positions['y2'] = (y2_x, y2_y)

        self.visible_space = ( (x2_x, x1_x), (y1_y, x1_y) )

    def calculate_visible_space(self):
        self.visible_space = ( (self.vertex_positions['x1'][0] + self.position[0], self.vertex_positions['x2'][0] - self.position[0]),    # max_x, min_x
                                (self.vertex_positions['x1'][1] + self.position[1], self.vertex_positions['y1'][1] - self.position[1]))  # max_y, min_y
