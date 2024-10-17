import socket

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
            print("Подключение к серверу...")
            self.create_socket()
            self.connect()
        except ConnectionError:
            print("Подключение оборвалось...")
            return False
        return True
