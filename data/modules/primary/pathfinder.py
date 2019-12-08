import copy


class Pathfinder:

    def __init__(self, map, screen):
        self.screen = screen
        self.map = map
        self.map_graph = []

    def setup_map_graph(self):
        map_graph = []
        line_graph = []
        for y in range(len(self.map.map)):
            for x in range(len(self.map.map[y])):
                big_position = (x * (75 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]),
                                y * (75 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1]))
                can_walk = self.can_walk_on_this_coordinate((x, y))
                node = Node((x, y), big_position)
                node.can_walk = can_walk
                line_graph.append(node)
            map_graph.append(line_graph)
            line_graph = []
        self.map_graph = map_graph

    def return_path(self, start_coordinate, destination_coordinate):
        start_node = self.get_node_by_coordinate(start_coordinate)
        destination_node = self.get_node_by_coordinate(destination_coordinate)

        if start_node is None or destination_node is None:
            return False
        if not destination_node.can_walk:
            destination_node = self.return_posibble_destination_node(destination_node)
            if not destination_node:
                return False

        start_node.f = g(start_node, destination_node) + manhattan_distance_heuristic(start_node, destination_node)
        open_list = [start_node]
        closed_list = []
        while len(open_list) > 0:
            current_index = self.return_smallest_f_cost_node_index(open_list)
            current = open_list[current_index]
            if tuple(current.coordinate) == tuple(destination_node.coordinate):
                return self.construct_path(destination_node)
            open_list.remove(current)
            closed_list.append(current)
            for neighbor in current.return_neighbors(self):
                if neighbor not in closed_list:
                    if neighbor not in open_list:
                        if neighbor.can_walk:
                            new_f = g(start_node, neighbor) + manhattan_distance_heuristic(
                                neighbor, destination_node)
                            neighbor.f = new_f
                            neighbor.parent = current
                            open_list.append(neighbor)
                        else:
                            new_f = g(start_node, neighbor) + manhattan_distance_heuristic(neighbor, destination_node)
                            if neighbor.f > new_f:
                                neighbor.f = new_f
                                neighbor.parent = current
        return False

    def can_walk_on_this_coordinate(self, coordinate_to_check: tuple):
        for person in self.screen.engine.loaded_game_resources.person_sprite_menager.sprites():
            if tuple(person.small_position) == coordinate_to_check:
                return False
        for _object in self.screen.engine.loaded_game_resources.objects_sprite_menager.sprites():
            if tuple(_object.small_position) == coordinate_to_check:
                return False
        return True

    def get_node_by_coordinate(self, coordinate):
        try:
            node = self.map_graph[coordinate[0]][coordinate[1]]
            return node
        except IndexError:
            return None

    def return_smallest_f_cost_node_index(self, node_list):
        min_f_index = 0
        for index in range(len(node_list)):
            if node_list[index].f < node_list[min_f_index].f:
                min_f_index = index
        return min_f_index

    def construct_path(self, destination_node):
        path = [destination_node]
        parent_node = destination_node.parent
        while parent_node is not None:
            if parent_node not in path:
                path.append(parent_node)
                parent_node = parent_node.parent
            else:
                path.reverse()
                return path
        path.reverse()
        return path

    def return_posibble_destination_node(self, destination_node):
        open_list = [_neighbor for _neighbor in destination_node.return_neighbors(self)]
        index = 0
        while True:
            if open_list[index].can_walk:
                return open_list[index]
            else:
                open_list += [_neighbor for _neighbor in open_list[index].return_neighbors(self)]
            index += 1


class Node:

    def __init__(self, coordinate, big_position):
        self.parent = None
        self.coordinate = coordinate
        self.big_position = big_position
        self.g = 1
        self.h = 0
        self.f = 0
        self.can_walk = True

    def return_neighbors(self, pathfinder):
        coordinates = ((self.coordinate[1] - 1, self.coordinate[0]), (self.coordinate[1] + 1, self.coordinate[0]),
                       (self.coordinate[1], self.coordinate[0] - 1), (self.coordinate[1], self.coordinate[0] + 1))

        neighbors = []
        for coordinate in coordinates:
            node = pathfinder.get_node_by_coordinate(coordinate)
            if node is not None:
                neighbors.append(node)
        return neighbors


def manhattan_distance_heuristic(starting_node, destination_node):
    dx = abs(starting_node.coordinate[0] - destination_node.coordinate[0])
    dy = abs(starting_node.coordinate[1] - destination_node.coordinate[1])
    return max(dx, dy)


def g(starting_node, destination_node):
    return 1
