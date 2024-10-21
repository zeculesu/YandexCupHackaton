from asyncio import sleep

import cv2

from config import MANIPULATOR_MOVE_CLAW
from Log_manager import Logs
from sender import Sender
import config as cfg
# from HighCamera import HighCamera
from result_type import Ok, result_type
import RobotCamera

import logging

"""

1) Обработка Exceptions

2) Value Detection - Sanya

3) Robots detection - AI

4) Walls detection %static%

5) Buckets detections %static%

6) Logs normal - throw all Exceptions

"""


class App:
    def __init__(self, color_robot):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.critical("Create Logs")
        self.color = color_robot

        t = 'rtsp://Admin:rtf123@192.168.2.250/251:554/1/1'
        l = "C:\\Aram\\UrFU\\FromVideo\\Left_1.avi"
        r = "C:\\Aram\\UrFU\\FromVideo\\Right_1.avi"
        Live_r = "http://192.168.2.156:8080/?action=stream"
        self.RobotCamera = RobotCamera.RobotCamera(Live_r)

    def run(self):

        while self.RobotCamera.make_iteration():
            pass

    def RunRobot(self):
        while True:
            high_camera_res = self.HighCamera.MakeIteration()

            if not high_camera_res:
                break

            # SENDER COMMAND
            """...
            angle = ...
            # message = MOTOR_STOP
            message = f"{MANIPULATOR_MOVE_CLAW} {angle}"
            if not sender.send_command(message):
                break"""

        return result_type(Ok(200))

    def startimage(self):
        for i in range(1, 20):
            print(i)
            self.HighCamera.Lol(f'screen{i}.png')


if __name__ == "__main__":
    host, port = "192.168.2.156", 4141
    sender = Sender(host, port)
    sender.try_connection()
    comm = f"{cfg.SET_COLOR_ROBOT} {cfg.ROBOT_COLOR}"
    sender.send_command(comm)
    # TODO ПР ЗАПУСКЕ СТАВИМ КАКОЙ ЦВЕТ
    App(color_robot=cfg.ROBOT_COLOR).run()