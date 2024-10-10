from sender import Sender

host = "192.168.2.156"
port = 2001


def go_moves(sender: Sender, param, n):
    sender.send_command("0201" + n)
    sender.send_command("0202" + n)
    if param == "forward":
        sender.send_command("000100")
    elif param == "reverse":
        sender.send_command("000200")
    elif param == "left":
        sender.send_command("000300")
    elif param == "right":
        sender.send_command("000400")


def arm_moves(sender: Sender, param):
    if param == "down":
        arm_down(sender)
    if param == "grab":
        arm_grab(sender)
    if param == "up":
        arm_up(sender)


def arm_down(sender: Sender):
    sender.send_command("0102ff")
    sender.send_command("010355")
    sender.send_command("010155")
    sender.send_command("010400")


def arm_up(sender: Sender):
    sender.send_command("010199")
    sender.send_command("010210")
    sender.send_command("010355")
    sender.send_command("010400")

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
            print("something went wrong:", e)
        command = input().split()


if __name__ == '__main__':
    print("Start robot control:")
    main(Sender(host, port))
    print("End robot control")
