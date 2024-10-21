import cv2
import numpy as np
import requests
from AI import AI


class RobotCamera:
    def __init__(self, index):
        self.indexCamera = index
        self.AI = AI()

    def read(self):
        global boobs
        stream = requests.get(self.indexCamera, stream=True)
        if stream.status_code == 200:
            boobs = bytes()
            for chunk in stream.iter_content(chunk_size=1024):
                boobs += chunk
                a = boobs.find(b'\xff\xd8')  # Начало jpeg
                b = boobs.find(b'\xff\xd9')  # Конец jpeg
                if a != -1 and b != -1:
                    jpg = boobs[a:b + 2]
                    boobs = boobs[b + 2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    return img

    def make_iteration(self):
        frame = self.read()

        if frame is not None:
            self.AI.live_ai(frame)
            return True
        else:
            return False