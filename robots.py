"""
James Gough coding challenge.
24/10/2021

Robots module that interprets JSON from a text file in order to provide the final coordinates of the robot's position
and bearing
"""
import json
from itertools import cycle
import re
import sys
import logging


class Robot:
    """
    Robot object that updates the position of the robot based on movement data received.
    Movement is updated through a class variable to allow for different bearing, axis and movement options.
    """

    bearings = ["north", "east", "south", "west"]
    movement_num_ref_list = list(range(len(bearings)))

    bearing_to_num_dict = dict(zip(bearings, movement_num_ref_list))
    turn_right = cycle(movement_num_ref_list)
    turn_left = cycle(movement_num_ref_list[::-1])

    movement_lookup_dict = {
        0: {"bearing": "north", "axis": "y", "movement": 1},
        1: {"bearing": "east", "axis": "x", "movement": 1},
        2: {"bearing": "south", "axis": "y", "movement": -1},
        3: {"bearing": "west", "axis": "x", "movement": -1},
    }

    def __init__(self, new_robot_json: dict):
        self.new_robot_json = new_robot_json

        self.current_robot_position = None
        self.bearing = None

        self.bearing_num = None
        self.movement_key = None
        self.y = None
        self.x = None

        self.robot_output_dict = None

    def add_initial_data(self):
        self.current_robot_position = self.new_robot_json["position"]
        self.x = self.current_robot_position["x"]
        self.y = self.current_robot_position["y"]

        self.bearing = self.new_robot_json["bearing"]
        self.bearing_num = self.bearing_to_num_dict[self.bearing]

    def cycle_to_initial_bearing_num(self):
        for i in self.turn_right:
            if i == self.bearing_num:
                break
        for i in self.turn_left:
            if i == self.bearing_num:
                break

    def change_direction(self, movement):
        """The momvement_key uses the movement_lookup_dict to determine how to update the robot's position"""
        direction = movement.split("-")[-1]
        if direction == "right":
            self.bearing_num = next(self.turn_right)
        else:
            self.bearing_num = next(self.turn_left)

    def move_forward(self):
        """Updates the coordinates via the movement_lookup_dict"""
        lookup_data = self.movement_lookup_dict[self.bearing_num]
        movement_value = lookup_data["movement"]
        axis = lookup_data["axis"]
        if axis == "x":
            self.x += movement_value
        else:
            self.y += movement_value

    def update_movement(self, move_command: dict):
        """
        Updates the current_status with the data contained in the move_command.
        :return:
        """
        movement = move_command.get("movement")
        if re.fullmatch(r"turn-\w+", movement):
            self.change_direction(movement)
        elif movement == "move-forward":
            self.move_forward()

    def provide_final_position(self):
        self.robot_output_dict = {
            "type": "robot",
            "position": {"x": self.x, "y": self.y},
            "bearing": self.movement_lookup_dict[self.bearing_num]["bearing"]
        }
        return self.robot_output_dict


class Asteroid:
    """
    Utilises the Robot and TextToDictConverter classes to loop through the entire text, allowing for multiple
    instances of Robot on the asteroid.
    """

    def __init__(self, new_asteroid_dict: dict):
        self.new_asteroid_dict = new_asteroid_dict
        self.asteroid_size_x = self.new_asteroid_dict["size"]["x"]
        self.asteroid_size_y = self.new_asteroid_dict["size"]["y"]

        self.asteroid_boundary = None

        self.robot_final_positions_list = None

        self.asteroid_boundary_warning = False

    def construct_asteroid_boundary(self):
        self.asteroid_boundary = {
            "x": {"max": self.asteroid_size_x, "min": self.asteroid_size_x * -1},
            "y": {"max": self.asteroid_size_y, "min": self.asteroid_size_y * -1}
        }

    def check_robot_within_boundary(self, _x, _y):
        if any([
            abs(_x) > self.asteroid_size_x,
            abs(_y) > self.asteroid_size_y
        ]):
            self.asteroid_boundary_warning = True


class AsteroidRobotDataParser:

    def __init__(self, _file_name):
        self.file_name = _file_name

        self.current_asteroid = None
        self.current_robot = None

        self.current_data_line = None
        self.data_type_parser = dict()

        self.boundary_warning = False

    def make_data_type_parser(self):
        self.data_type_parser = {
            "asteroid": self.parse_type_asteroid,
            "new-robot": self.parse_type_robot,
            "move": self.parse_type_move
        }

    def parse_type_asteroid(self):
        self.current_asteroid = Asteroid(self.current_data_line)

    def print_final_position(self):
        if self.current_robot:
            print(self.current_robot.provide_final_position())

    def parse_type_robot(self):
        self.print_final_position()
        self.current_robot = Robot(self.current_data_line)
        self.current_robot.add_initial_data()
        self.current_robot.cycle_to_initial_bearing_num()

    def parse_type_move(self):
        self.current_robot.update_movement(self.current_data_line)
        self.current_asteroid.check_robot_within_boundary(self.current_robot.x, self.current_robot.y)
        if self.current_asteroid.asteroid_boundary_warning:
            logging.warning(f"""Robot has gone beyond the bounds of the asteroid! 
                Current coordinates are: {self.current_robot.x}, {self.current_robot.y}
                """)

    def parse_data_line_by_type(self):
        self.make_data_type_parser()
        data_type = self.current_data_line["type"]
        self.data_type_parser[data_type]()

    def run_data_parser(self):
        with open(self.file_name) as file:
            for line in file:
                self.current_data_line = json.loads(line)
                self.parse_data_line_by_type()
        self.print_final_position()


if __name__ == "__main__":
    file_name = sys.argv[-1]
    if not re.fullmatch(r".*.txt", file_name):
        file_name = "instructions"
    file_name = file_name.split(".")[0]
    data_parser = AsteroidRobotDataParser(file_name)
    data_parser.run_data_parser()
