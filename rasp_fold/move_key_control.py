from time import sleep

from YandexCupHackaton.rasp_fold.main_dir import servo, motor

commands = ["forward", "backward", "right_on_place", "left_on_place", "right", "left"]
mc = motor_controller.MotorController()

while True:
    sc = servo_controller.ServoController()
    sleep(5)
    sc.open_claw()
    sc.set_down_position()
    sleep(5)
    sc.set_throw_position()
    sc.open_claw()
    sleep(5)

while True:
    inp_command = input().split()
    try:
        func = inp_command[0]
        if func == "forward":
            mc.forward_on_steps(int(inp_command[1]))
        elif func == "backward":
            mc.backward_on_steps(int(inp_command[1]))
        elif func == "right":
            mc.right_forward_on_steps(int(inp_command[1]))
        elif func == "right_back":
            mc.right_backward_on_steps(int(inp_command[1]))
        elif func == "left":
            mc.left_forward_on_steps(int(inp_command[1]))
        elif func == "left_back":
            mc.left_backward_on_steps(int(inp_command[1]))
        elif func == "right_on_place":
            mc.right_on_place_on_steps(int(inp_command[1]))
        elif func == "left_on_place":
            mc.left_on_place_on_steps(int(inp_command[1]))
        elif func == "exit":
            break
    except Exception as e:
        print("unknown command", e)
