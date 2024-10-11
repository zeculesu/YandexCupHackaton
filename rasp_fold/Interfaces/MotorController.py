from YandexCupHackaton.rasp_fold import xr_motor
from time import sleep

STEP_TIME = 0.2
DEFAULT_SPEED = 30
robotDir = xr_motor.RobotDirection()


def forward(n):
    robotDir.set_speed(1, DEFAULT_SPEED)
    robotDir.set_speed(2, DEFAULT_SPEED)
    robotDir.forward()
    sleep(STEP_TIME * n)
    robotDir.stop()


def backward(n):
    robotDir.set_speed(1, DEFAULT_SPEED)
    robotDir.set_speed(2, DEFAULT_SPEED)
    robotDir.back()
    sleep(STEP_TIME * n)
    robotDir.stop()


def right_on_place(n):
    robotDir.set_speed(1, DEFAULT_SPEED)
    robotDir.set_speed(2, DEFAULT_SPEED)
    robotDir.right()
    sleep(STEP_TIME * n)
    robotDir.stop()


def left_on_place(n):
    robotDir.set_speed(1, DEFAULT_SPEED)
    robotDir.set_speed(2, DEFAULT_SPEED)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()


def right(n):
    robotDir.set_speed(1, DEFAULT_SPEED)
    robotDir.set_speed(2, 0)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()


def left(n):
    robotDir.set_speed(1, 0)
    robotDir.set_speed(2, DEFAULT_SPEED)
    robotDir.left()
    sleep(STEP_TIME * n)
    robotDir.stop()
