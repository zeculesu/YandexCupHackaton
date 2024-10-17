from asyncio import sleep

from sympy.physics.units import stefan_boltzmann_constant

from AppOpenCv.App.command_enum import Manipulator, Motor
from AppOpenCv.App.config import MANIPULATOR_MOVE_CLAW
from Log_manager import Logs
import result_type as ResType
from sender import Sender
from HighCamera import HighCamera

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
    def __init__(self):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.info("Create Logs")

        t = 'rtsp://Admin:rtf123@192.168.2.250/251:554/1/1'
        l = "C:\\Aram\\UrFU\\FromVideo\\Left_1.avi"
        r = "C:\\Aram\\UrFU\\FromVideo\\Right_1.avi"
        self.HighCamera = HighCamera(l)

    def run(self):
        from time import sleep

        zaderjka = 10
        while True:
            high_camera_res = self.HighCamera.MakeIteration()

            if not high_camera_res:
                break

            sender = Sender(host, port)
            if not sender.try_connection():
                break

            # SENDER COMMAND
            ...
            angle = ...
            # message = MOTOR_STOP
            message = f"{MANIPULATOR_MOVE_CLAW} {angle}"
            if not sender.send_command(message):
                break

        return ResType.result_type(ResType.Ok(200))
      
    def startimage(self):
        for i in range(1, 20):
            print(i)
            self.HighCamera.Lol(f'screen{i}.png')



if __name__ == "__main__":
    host, port = "192.168.2.156", 4141
    App().run()
    App().startimage()

