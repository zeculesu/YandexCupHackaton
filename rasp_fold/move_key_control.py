import motor_controller

commands = ["forward", "backward", "right_on_place", "left_on_place", "right", "left"]
mc = motor_controller.MotorController()

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
