from buzzer import Buzzer
from camera import CameraController
from manipulator import ManipulatorController
from motor import MotorController
from rgb_panel import RGBPanel
from server import Jesys

motor = MotorController()
camera = CameraController()
manipulator = ManipulatorController()
rgb = RGBPanel()
beep = Buzzer()
server = Jesys(motor, camera, manipulator)

# TODO раскидать по папочкам
# TODO сделать освобождение порта
# TODO вынести порт и адрес в отдельный конфиг
host, port = "192.168.2.156", 4242
print("Start")
server.start_server()
