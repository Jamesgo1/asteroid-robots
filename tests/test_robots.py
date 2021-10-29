"""
Test suite for robots.py program.
"""
import robots

TEST_TXT_FILE = r"test_input"
SAMPLE_NEW_ROBOT = {'type': 'new-robot', 'position': {'x': 1, 'y': 2}, 'bearing': 'north'}
SAMPLE_TURN_COMMAND = {'type': 'move', 'movement': 'turn-left'}
SAMPLE_MOVE_COMMAND = {'type': 'move', 'movement': 'move-forward'}

SAMPLE_FINAL_POSITION = [{"type": "new-robot", "position": {"x": 1, "y": 2}, "bearing": "north"},
                         {"type": "move", "movement": "turn-left"},
                         {"type": "move", "movement": "move-forward"},
                         {"type": "move", "movement": "turn-left"},
                         {"type": "move", "movement": "move-forward"},
                         {"type": "move", "movement": "turn-left"},
                         {"type": "move", "movement": "move-forward"},
                         {"type": "move", "movement": "turn-left"},
                         {"type": "move", "movement": "move-forward"},
                         {"type": "move", "movement": "move-forward"}]

SAMPLE_ASTEROID = {'type': 'asteroid', 'size': {'x': 10, 'y': 20}}


def test_add_initial_data():
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    assert robot.bearing == "north"
    assert robot.current_robot_position == {'x': 1, 'y': 2}
    assert robot.bearing_num == 0


def test_cycle_to_initial_bearing_num():
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    if robot.bearing_num == robot.movement_num_ref_list[-1]:
        assert next(robot.turn_right) == 0
    else:
        assert robot.bearing_num + 1 == next(robot.turn_right)


def test_update_movement():
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.update_movement(SAMPLE_TURN_COMMAND)


def test_update_movement_direction():
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot.update_movement(SAMPLE_TURN_COMMAND)

    assert robot.bearing_num == 3


def test_update_movement_move_forward_north():
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot.update_movement(SAMPLE_MOVE_COMMAND)

    assert robot.y == 3


def test_update_movement_move_forward_east():
    SAMPLE_NEW_ROBOT["bearing"] = "east"
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot.update_movement(SAMPLE_MOVE_COMMAND)

    assert robot.x == 2


def test_update_movement_move_forward_south():
    SAMPLE_NEW_ROBOT["bearing"] = "south"
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot.update_movement(SAMPLE_MOVE_COMMAND)

    assert robot.x == 1


def test_update_movement_move_forward_west():
    SAMPLE_NEW_ROBOT["bearing"] = "west"
    robot = robots.Robot(SAMPLE_NEW_ROBOT)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot.update_movement(SAMPLE_MOVE_COMMAND)

    assert robot.x == 0


def test_final_position():
    new_robot_data = SAMPLE_FINAL_POSITION[0]
    robot = robots.Robot(new_robot_data)
    robot.add_initial_data()
    robot.cycle_to_initial_bearing_num()

    robot_commands = SAMPLE_FINAL_POSITION[1:]
    for cmd in robot_commands:
        robot.update_movement(cmd)
    final_pos = robot.provide_final_position()
    assert final_pos == {"type": "robot", "position": {"x": 1, "y": 3}, "bearing": "north"}


def test_construct_asteroid_boundary():
    asteroid = robots.Asteroid(SAMPLE_ASTEROID)
    asteroid.construct_asteroid_boundary()
    assert asteroid.asteroid_boundary == {
        "x": {"max": 10, "min": -10},
        "y": {"max": 20, "min": -20}
    }
