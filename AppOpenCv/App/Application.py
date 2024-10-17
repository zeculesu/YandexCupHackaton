from Log_manager import Logs
import result_type as ResType

from HighCamera import HighCamera

import logging


class App:
    def __init__(self):
        LogClass = Logs()
        self.logger = LogClass.getLogger()
        self.logger.info("Create Logs")

        self.HighCamera = HighCamera("../../../Right_1.avi")

    def run(self):
        while True:
            high_camera_res = self.HighCamera.MakeIteration()
            
            if not high_camera_res:
                break
            
        return ResType.result_type(ResType.Ok(200))    


if __name__ == "__main__":
    App().run()
