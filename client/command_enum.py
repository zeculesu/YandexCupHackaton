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
    pass

class Camera(Enum):
    pass