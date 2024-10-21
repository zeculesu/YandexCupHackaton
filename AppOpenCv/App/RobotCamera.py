import threading
from time import sleep

import cv2
import numpy as np
import requests
import multiprocessing as mp

class RobotCamera(object):

    def find_red_cube(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170, 100, 100])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        mask = mask1 + mask2

        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        center = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        return center

    def __init__(self):
        self.thread = threading.Thread(target=self.start_read)
        self.thread.daemon = True
        self.thread.start()
        self.lock = threading.Lock()
        self.frame = None
        self.center = None

    def start_read(self):
        global boobs
        stream = requests.get("http://192.168.2.156:8080/?action=stream", stream=True)
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

                    center = self.find_red_cube(img)
                    if center is not None:
                        cv2.circle(img, center, 5, (0, 255, 0), -1)
                        cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 0, 255), 2)

                    cv2.imshow('img', img)
                    self.frame = img
                    with self.lock:
                        self.center = center
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

    def get_center(self):
        with self.lock:
            return self.center

camera = RobotCamera()
for i in range(10**9):
    print(camera.get_center())
    sleep(0.5)