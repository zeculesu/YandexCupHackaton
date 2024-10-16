import socket


class Sender:
    command_list_motor = {
        "stop": 0,
        "forward": 1,
        "backward": 2,
        "right_on_place": 3,
        "left_on_place": 4,
        "right_forward": 5,
        "right_backward": 6,
        "left_forward": 7,
        "left_backward": 8,
    }

    command_list_manipulator = {

    }

    command_list_camera = {

    }

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if self.socket is None:
            self.create_socket()
        self.socket.connect((self.host, self.port))

    def socket_close(self):
        self.socket.close()
        self.socket = None

    # Sender.send_motor("stop")
    def send_motor(self, command):
        self.send(Sender.command_list_motor[command])

    def send_manipulator(self, command):
        self.send(Sender.command_list_manipulator[command])

    def send_camera(self, command):
        self.send(Sender.command_list_camera[command])

    def send(self, message):
        self.socket.send(message.encode('utf-8'))
