import Buttons

import cv2 as cv
import numpy as np


class VideoCamera:
    def __init__(self, index: str):
        self.index = index
        self.frame_counter = 1

        self.VideoCap = cv.VideoCapture(self.index)

    def IsOpen(self) -> bool:
        return self.VideoCap.isOpened()

    def read(self):
        return self.VideoCap.read()

    def getFrameCount(self) -> int:
        return self.frame_counter

    def raiseCount(self) -> None:
        self.frame_counter += 1
