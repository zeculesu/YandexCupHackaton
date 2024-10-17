from AppOpenCv.App.config import *
from old.sender import Sender

sender = Sender("192.168.2.156", 4141)
sender.start_client()
# exec(open("send_command_console_python.py").read())