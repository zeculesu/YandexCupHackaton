from ..interfaces import motor_controller

commands = ["forward", "backward", "right_on_place", "left_on_place", "right", "left"]

while True:
    inp_command = input().split()
    try:
        func = inp_command[0]
        if func == "forward":
            motor_controller.forward(inp_command[1])
        elif func == "backward":
            motor_controller.backward(inp_command[1])
        elif func == "right":
            motor_controller.right(inp_command[1])
        elif func == "left":
            motor_controller.left(inp_command[1])
        elif func == "right_on_place":
            motor_controller.right_on_place(inp_command[1])
        elif func == "left_on_place":
            motor_controller.left_on_place(inp_command[1])
        elif func == "exit":
            break
    except Exception:
        print("unknown command")
