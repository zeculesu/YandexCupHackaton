from asyncio import sleep

from AppOpenCv.App.command_enum import Manipulator
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
            if not sender.start_client():
                sender.try_connection()

            if not sender.check_connection():
                self.logger.error("Connection Error")

            # SENDER COMMAND
            ...
            angle = ...
            message = f"{Manipulator.MOVE_CLAW} {angle}"
            if sender.check_connection():
                resp = sender.send(message)
                if not resp:
                    self.logger.warning("no response from server")
                    sender.try_connection()
                else:
                    self.logger.info(f"answer from server: {resp}")
            else:
                self.logger.warning("no response from server")
                sender.try_connection()

        return ResType.result_type(ResType.Ok(200))


if __name__ == "__main__":
    host, port = "192.168.2.156", 4141
    App().run()
