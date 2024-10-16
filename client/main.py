import time

from client.sender import Sender


def start_client():
    sender = Sender(host, port)
    try:
        print("Подключение к серверу...")
        sender.create_socket()
        sender.connect()
    except ConnectionError:
        print("Подключение оборвалось...")
        time.sleep(5)
        return

    print("Подключение к серверу прошло успешно")
    while True:
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break

        sender.send(message)
        response = sender.socket.recv(1024).decode('utf-8')
        if not response:
            print("Подключение оборвалось...")
            sender.socket_close()
            return
        print(f"Ответ от сервера: {response}")

    sender.socket_close()


if __name__ == "__main__":
    host, port = "192.168.2.156", 4242
    print("Начало работы")
    while True:
        start_client()
