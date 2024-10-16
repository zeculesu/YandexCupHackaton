from buzzer import Buzzer
import infrared
import ultrasonic
from rgb_panel import RGBPanel
from motor import MotorController
from camera import CameraController
from manipulator import ManipulatorController

import config as cfg
from time import sleep

motor = MotorController()
manipulator = ManipulatorController()
camera = CameraController()
buzzer = Buzzer()
rgb_panel = RGBPanel()
try:
    oled = Oled()
    oled.disp_default()
    oled.disp_cruising_mode()
except:
    print("oled init fail")

print("pupupu")
print("all init")
sleep(5)
print("im here")
manipulator.set_throw_position()
print("im almost here")
sleep(2)
print("zhest`")
manipulator.open_claw()
