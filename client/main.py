import time

from AppOpenCv.App.sender import Sender

host, port = "192.168.2.156", 4141

sender = Sender(host, port)
while True:
    try:
        if sender.start_client():
            while True:
                mess = input("Введите команду: ")
                resp = sender.send(mess)
                if not resp:
                    break
                print(f"Ответ от сервера: {resp}")
        else:
            time.sleep(5)
    except KeyboardInterrupt:
        break
