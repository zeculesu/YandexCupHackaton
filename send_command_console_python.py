import socket
from time import sleep


# пишем sender = Sender(self.host, self.port) потом
# sender.start_client(), проверяем если там не False, то всё хорошо, мы подключились
# далее чтобы отправить запрос пишем sender.send( MOTOR.STOP (например) ) если произошла ошибка при отправке сообщения,
# то вернет False
# в САМОМ конце работы надо закрыть сокет с помощью sender.socket_close()


class Sender:
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
        if self.socket is not None:
            self.socket.close()
        self.socket = None

    def send(self, message):
        self.socket.send(message.encode('utf-8'))
        response = self.socket.recv(1024).decode('utf-8')
        if not response:
            self.socket_close()
            return False
        return response

    def start_client(self):
        try:
            self.create_socket()
            self.connect()
        except ConnectionError:
            self.socket_close()
            return False

        return True

    def try_connection(self):
        for i in range(5):
            if self.start_client():
                return True
            sleep(5)
        return False

    def check_connection(self):
        return True if self.socket else False

    def send_command(self, command):
        if not self.check_connection():
            if not self.try_connection():
                return False
        resp = self.send(command)
        return self.handle_response(resp, command)

    def handle_response(self, resp, command):
        if not resp:
            if not self.try_connection():
                return False
            resp = self.send(command)
            if not resp:
                return False
        return True


sender = Sender("192.168.2.156", 4141)
sender.start_client()
while True:
    comm = input()
    if comm == "exit":
        break
    print(sender.send_command(comm))
# exec(open("send_command_console_python.py").read())
