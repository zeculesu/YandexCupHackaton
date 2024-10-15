from motor import MotorController
import infrared
import buzzer
from manipulator import ManipulatorController

manipulator = ManipulatorController()
motor = MotorController()
beep = buzzer.Buzzer()
step = 2
waiting = False
while True:
    left_ir, right_ir, middle_ir = infrared.get_left_value(), infrared.get_right_value(), infrared.get_middle_value()
    left_line_ir, right_line_ir = infrared.get_left_line_value(), infrared.get_right_line_value()
    if left_ir and right_ir and middle_ir:
        waiting = False

    # if left_line_ir == 0:
    #     motor.left_forward(step)
    # if right_line_ir == 0:
    #     motor.right_forward(step)
    # if not (left_line_ir or right_line_ir):
    #     motor.backward(8)
    #     motor.right_backward(8)

    if left_ir == 0:
        motor.stop()
        if middle_ir == 1:
            waiting = False
            motor.backward(10)
        else:
            waiting = True
            beep.play_music(0, beep.melody_Happy_birthday, beep.beet_Happy_birthday)
        motor.left_on_place(step * 8)
    if right_ir == 0:
        motor.stop()
        if middle_ir == 1:
            waiting = False
            motor.backward(15)
        else:
            waiting = True
            beep.play_music(0, beep.melody_Happy_birthday, beep.beet_Happy_birthday)
        motor.right_on_place(step * 8)
    if waiting == False:
        motor.forward(step)
