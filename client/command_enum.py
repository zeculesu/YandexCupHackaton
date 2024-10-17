from enum import Enum


class Motor(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    RIGHT_ON_PLACE = 3
    LEFT_ON_PLACE = 4
    RIGHT_FORWARD = 5
    RIGHT_BACKWARD = 6
    LEFT_FORWARD = 7
    LEFT_BACKWARD = 8


class Manipulator(Enum):
    DEFAULT_POSITION = 9
    CLOSE_CLAW = 10
    OPEN_CLAW = 11
    SET_THROW_POSITION = 12
    SET_DOWN_POSITION = 13
    MOVE_MAIN = 14
    MOVE_CUBIT = 15
    MOVE_WRIST = 16
    MOVE_CLAW = 17


class Camera(Enum):
    DEFAULT_POSITION = 18
    MOVE_CUBIT = 19
    MOVE_ROTATE = 20
