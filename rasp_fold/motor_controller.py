import xr_motor
from time import sleep

from xr_motor import RobotDirection

STEP_TIME = 0.1
DEFAULT_SPEED = 30

class MotorController(RobotDirection) :
    def forward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_forward()
        sleep(STEP_TIME * n)
        self.stop()

    def backward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_reverse()
        sleep(STEP_TIME * n)
        self.stop()


    def right_on_place_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_reverse()
        sleep(STEP_TIME * n)
        self.stop()

    def left_on_place_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_forward()
        sleep(STEP_TIME * n)
        self.stop()

    def right_forward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_forward()
        self.m3m4_stop()
        sleep(STEP_TIME * n)
        self.stop()

    def right_backward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m1m2_reverse()
        self.m3m4_stop()
        sleep(STEP_TIME * n)
        self.stop()

    def left_forward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m3m4_forward()
        self.m1m2_stop()
        sleep(STEP_TIME * n)
        self.stop()

    def left_backward_on_steps(self, n):
        self.set_both_speed(DEFAULT_SPEED, DEFAULT_SPEED)
        self.m3m4_reverse()
        self.m1m2_stop()
        sleep(STEP_TIME * n)
        self.stop()

    def set_both_speed(self, left_speed, right_speed):
        self.set_speed(1, left_speed)
        self.set_speed(2, right_speed)

# def forward(n):
#     robotDir.forward()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def backward(n):
#     robotDir.back()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def right_on_place(n):
#     robotDir.right()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def left_on_place(n):
#     robotDir.left()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def right_forward(n):
#     robotDir.right()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def left(n):
#     robotDir.left()
#     sleep(STEP_TIME * n)
#     robotDir.stop()
#
#
# def set_speed(left_motor, right_motor):
#     robotDir.set_speed(1, left_motor)
#     robotDir.set_speed(2, right_motor)
