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
motor.right_on_place()
motor.right_on_place()
motor.right_on_place()
motor.right_on_place()
rgb.set_all([cfg.GREEN] * 8)
motor.forward(20)
motor.left_on_place()
motor.left_on_place()
motor.left_on_place()
rgb.set_all([cfg.RED] * 8)

motor.forward(45)

for i in range(13):
    motor.left_on_place()
#server.start_server()
