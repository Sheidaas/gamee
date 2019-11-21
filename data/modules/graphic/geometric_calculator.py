import math


class Calculator:

    def return_visible_positions(self, player, size):
        potentially_square = []
        player_position = player.coordinate

        min_x = player_position[0] - player.statistics.sight - 1
        max_x = player_position[0] + player.statistics.sight + 1

        min_y = player_position[1] - player.statistics.sight - 1
        max_y = player_position[1] + player.statistics.sight + 1

        if min_y < 0:
            min_y = 0
        if min_x < 0:
            min_x = 0

        if max_y > size['y']:
            max_y = size['y']


        if max_x > size['x']:
            max_x = size['x']

        visible_square = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if self.is_square_in_vision((x, y), player):
                    visible_square.append((x, y))

        return visible_square

    @staticmethod
    def is_square_in_vision(square, player):
        distance = math.sqrt(math.pow(square[0] - player.coordinate[0], 2) + math.pow(square[1] - player.coordinate[1], 2))
        if distance < player.statistics.sight:
            return True
        return False

    @staticmethod
    def is_object_in_vision(obj_coordinate, visible_square, image_coordinate):
        for x in range(len(visible_square)):
            if visible_square[x][0] == obj_coordinate[0] and visible_square[x][1] == obj_coordinate[1]:
                return image_coordinate[x]
        return None

    @staticmethod
    def is_object_in_area(obj_coordinate, player_coordinate):
        distance = math.sqrt(math.pow(obj_coordinate[0] - player_coordinate[0], 2)
                             + math.pow(obj_coordinate[1] - player_coordinate[1], 2))
        if distance < 1.5:
            return True
        return False

    @staticmethod
    def calculate_squares_positions(player, resolution, scale, squares):
        positions = []
        size = (75 * scale[0], 75 * scale[1])
        for position in squares:
            new_x = (position[0] * size[0] - (player.coordinate[0] * size[0]) + (resolution[0] / 2) - 50)
            new_y = (position[1] * size[1] - (player.coordinate[1] * size[1]) + (resolution[1] / 2) - 75)
            positions.append((new_x, new_y))
        return positions
