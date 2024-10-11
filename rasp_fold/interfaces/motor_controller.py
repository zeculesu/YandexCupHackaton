from .. import xr_motor
from time import sleep

STEP_TIME = 0.2
DEFAULT_SPEED = 30
robotDir = xr_motor.RobotDirection()
robotDir.stop()


def forward(n):
    set_speed(DEFAULT_SPEED, DEFAULT_SPEED)
    robotDir.forward()
    sleep(STEP_TIME * n)
    robotDir.stop()


def backward(n):
    set_speed(DEFAULT_SPEED, DEFAULT_SPEED)
    robotDir.back()
    sleep(STEP_TIME * n)
    robotDir.stop()


def right_on_place(n):
    set_speed(DEFAULT_SPEED, DEFAULT_SPEED)
    robotDir.right()
    sleep(STEP_TIME * n)
    robotDir.stop()


def left_on_place(n):
    set_speed(DEFAULT_SPEED, DEFAULT_SPEED)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()


def right(n):
    set_speed(DEFAULT_SPEED, 0)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()


def left(n):
    set_speed(0, DEFAULT_SPEED)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()


def set_speed(left_motor, right_motor):
    robotDir.set_speed(1, left_motor)
    robotDir.set_speed(2, right_motor)
