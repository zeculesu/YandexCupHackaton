from time import sleep

from config import *
from sender import Sender
from time import sleep

host, port = "192.168.2.156", 4141

sender = Sender(host, port)
print(sender.start_client())
sender.send("14")
sender.send("12")
sleep(5)
sender.send("19")
# while True:
#     try:
#         if sender.start_client():
#             while True:
#                 mess = input("Введите команду: ")
#                 resp = sender.send(mess)
#                 if not resp:
#                     break
#                 print(f"Ответ от сервера: {resp}")
#         else:
#             time.sleep(5)
#     except KeyboardInterrupt:
#         break
