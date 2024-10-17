from old.sender_example import Sender

host = "192.168.2.156"
port = 2001


def go_moves(sender: Sender, param, n):
    sender.send_command("0201" + n)
    sender.send_command("0202" + n)
    command_code = {"forward": "000100",
                    "reverse": "000200",
                    "left": "000300",
                    "right": "000400"}
    if param in command_code:
        sender.send_command(command_code[param])


def arm_moves(sender: Sender, param):
    if param == "down":
        arm_down(sender)
    if param == "grab":
        arm_grab(sender)
    if param == "up":
        arm_up(sender)


def arm_down(sender: Sender):
    for command in ["0102ff", "010355", "010155", "010420"]:
        sender.send_command(command)


def arm_up(sender: Sender):
    for command in ["010199", "010210", "010355", "010420"]:
        sender.send_command(command)


def arm_grab(sender: Sender):
    sender.send_command("010470")
    sender.send_command("0101aa")


def main(sender: Sender):
    command = input().split()
    while command != ["exit"]:
        try:
            print("command: ", *command)
            if command[0] == "arm":
                arm_moves(sender, command[1])
            elif command[0] == "go":
                go_moves(sender, command[1], command[2])
            else:
                sender.send_command(''.join(command))
        except Exception as e:
            print("Something went wrong:", e)
        command = input().split()


if __name__ == '__main__':
    print("Start robot control:")
    main(Sender(host, port))
    print("End robot control")
