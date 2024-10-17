import signal
import socket
import sys

class Server:
    def __init__(self, port, motor, camera, manipulator):
        self.port = port
        self.motor = motor
        self.manipulator = manipulator
        self.camera = camera

        self.server_socket = None
        signal.signal(signal.SIGINT, self.signal_handler)

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)

            print("Сервер запущен, ожидается подключение...")

            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Подключено: {addr}")
                self.handle_client(client_socket)
        except Exception as e:
            self.server_socket.close()
            print(e)
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Получено сообщение: {message}")
                self.read_request(message)
                client_socket.send("Сообщение получено".encode('utf-8'))
            except Exception as e:
                print(e)
        client_socket.close()

    def signal_handler(self, sig, frame):
        print("Завершение сервера...")
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)

    def read_request(self, command):
        try:
            command_line = list(map(int, command.split()))
            if len(command_line) == 2:
                command, val = command_line
            else:
                command = command_line[0]

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

            elif 9 <= command <= 17:
                if command == 9:
                    self.manipulator.set_default_position()

                elif command == 10:
                    self.manipulator.close_claw()

                elif command == 11:
                    self.manipulator.open_claw()

                elif command == 12:
                    self.manipulator.set_throw_position()

                elif command == 13:
                    self.manipulator.set_down_position()

                elif command == 14:
                    self.manipulator.move_main(val)

                elif command == 15:
                    self.manipulator.move_cubit(val)

                elif command == 16:
                    self.manipulator.move_wrist(val)

                elif command == 17:
                    self.manipulator.move_claw(val)

            elif 18 <= command <= 20:
                if command == 18:
                    self.camera.set_default_position()
                elif command == 19:
                    self.camera.move_cubit(val)
                elif command == 20:
                    self.camera.move_rotate(val)
        except Exception as e:
            return
