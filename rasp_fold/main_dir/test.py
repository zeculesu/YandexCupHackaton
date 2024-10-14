from time import sleep

import motor
import servo

mc = motor.MotorController()
sc = servo.ServoController()

command = int(input())
while command != 0:
    sc.set(8, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(7, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(6, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(5, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(4, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(3, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(2, command)
    command = int(input())

command = int(input())
while command != 0:
    sc.set(1, command)
    command = int(input())

mc.forward_on_steps(3)
mc.right_on_place_on_steps(3)
mc.left_on_place_on_steps(3)
mc.backward_on_steps(3)

sc.open_claw()
sc.set_default_position()
sleep(2)
sc.set_down_position()
sc.open_claw()
sleep(2)
sc.set_throw_position()
