from sender import Sender

host = "192.168.1.109"
port = 2001


def main(sender: Sender):
    command = input().split()
    while command != ["exit"]:
        try:
            print("command: ", *command)
            sender.send_command(''.join(command))
        except Exception as e:
            print("something went wrong:", e)
        command = input().split()


if __name__ == '__main__':
    print("Start robot control:")
    main(Sender(host, port))
    print("End robot control")
