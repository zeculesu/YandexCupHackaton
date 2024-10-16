import socket

port = 4242

class Jesys:
    def __init__(self, motor, manipulator, camera):
        self.motor = motor
        self.manipulator = manipulator
        self.camera = camera

    def start_server(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(5)

            print("Сервер запущен, ожидается подключение...")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Подключено: {addr}")
                self.handle_client(client_socket)
        except Exception as e:
            server_socket.close()
            print(e)

    def handle_client(self, client_socket):
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Получено сообщение: {message}")
            self.read_request(message)
            client_socket.send("Сообщение получено".encode('utf-8'))
        client_socket.close()

    def read_request(self, command):
        command = int(command)
        if 0 <= command <= 8:
            if command == 0:
                self.motor.stop()
            elif command == 1:
                self.motor.forward()
            elif command == 2:
                self.motor.backward()
            elif command == 3:
                self.motor.right_on_place()
            elif command == 4:
                self.motor.left_on_place()
            elif command == 5:
                self.motor.right_forward()
            elif command == 6:
                self.motor.right_backward()
            elif command == 7:
                self.motor.left_forward()
            elif command == 8:
                self.motor.left_backward()

#
# if __name__ == "__main__":
#     host, port = "192.168.2.156", 4242
#     start_server()
