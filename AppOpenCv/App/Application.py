from asyncio import sleep

from sympy.physics.units import stefan_boltzmann_constant

from AppOpenCv.App.command_enum import Manipulator, Motor
from AppOpenCv.App.config import MANIPULATOR_MOVE_CLAW
from Log_manager import Logs
import result_type as ResType
from sender import Sender
from HighCamera import HighCamera

import logging


class App:
    def __init__(self):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.info("Create Logs")

        self.HighCamera = HighCamera("C:\\Aram\\UrFU\\FromVideo\\Right_1.avi")

    def run(self):
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


if __name__ == "__main__":
    host, port = "192.168.2.156", 4141
    App().run()
