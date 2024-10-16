import socket
import time


def start_client():
    try:
        print("Подключение к серверу...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    except ConnectionError:
        print("Подключение оборвалось...")
        time.sleep(5)
        start_client()

    print("Подключение к серверу прошло успешно")
    while True:
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if not response:
            print("Подключение оборвалось...")
            client_socket.close()
            start_client()
        print(f"Ответ от сервера: {response}")

    client_socket.close()


if __name__ == "__main__":
    host, port = "192.168.2.156", 4242
    print("Начало работы")
    start_client()
