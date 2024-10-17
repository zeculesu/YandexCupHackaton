import time

from client.sender import Sender
import workspace_rsp.config as cfg

host, port = "192.168.2.156", cfg.PORT

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
