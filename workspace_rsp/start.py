from buzzer import Buzzer
from camera import CameraController
from manipulator import ManipulatorController
from motor import MotorController
from rgb_panel import RGBPanel
from server import Server
import config as cfg

motor = MotorController()
camera = CameraController()
manipulator = ManipulatorController()
rgb = RGBPanel()
beep = Buzzer()
port = cfg.PORT

server = Server(port, motor, camera, manipulator, rgb)

# TODO раскидать по папочкам

print("Start")
server.start_server()