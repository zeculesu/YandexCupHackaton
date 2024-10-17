from client.sender import Sender

host, port = "192.168.2.156", 4242
sender = Sender(host, port)
while True:
    try:
        is_connect =  sender.start_client()
        if is_connect:
            break
    except:
        continue


