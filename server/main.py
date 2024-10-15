import socket


def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)

        print("Сервер запущен, ожидается подключение...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Подключено: {addr}")
            handle_client(client_socket)
    except Exception as e:
        print(e)
        start_server()


def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"Получено сообщение: {message}")
        client_socket.send("Сообщение получено".encode('utf-8'))
    client_socket.close()


if __name__ == "__main__":
    host, port = "192.168.2.156", 4242
    start_server()
