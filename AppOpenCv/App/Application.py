import logging
import VideoCamera as Camera
import result_type as ResType
import Log 

class App:
    def __init__(self):
        self.VideoCameraOnRobot = Camera.VideoCamera('http://192.168.2.156:8080/?action=stream')
        self.VideoCameraOnHigh = Camera.VideoCamera('')
        
        self.Logs = Log.Logs()
        logging.info("Create Logs")

    def run(self) -> ResType.result_type[int, str]:
        logging.info("Start Application")

    
        return ResType.result_type(ResType.Error("res"))    
