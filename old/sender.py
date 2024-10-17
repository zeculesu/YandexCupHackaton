import socket
import time


class Sender:
    header = "ff"

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_command(self, command: str):
        try:
            cur_command = bytes.fromhex(Sender.header + command + Sender.header)
            # Создаем сокет
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)

            # Устанавливаем соединение
            s.connect((self.host, self.port))

            # Отправляем команду
            s.sendall(cur_command)

            # Добавляем небольшой задержку между отправками команд
            time.sleep(1)

            return True
        except socket.error as e:
            print(f"Error socket: {e}")
            return False
        finally:
            # Закрываем соединение
            s.close()
