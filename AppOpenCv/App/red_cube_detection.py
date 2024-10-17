import asyncio
from pyexpat.errors import messages
from time import sleep

import cv2
import numpy as np
import requests
from numpy.lib.function_base import select

from old.sender import send_command
from sender_without_logger import Sender
import config as cfg

async def send_move(sender, move):
    print(2)
    sender.send_command(move)
    print(3)

# from AppOpenCv.App.sender import Sender
def find_red_cube(frame):
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

def run():
    global bytes
    sender = Sender("192.168.2.156", 4141)
    sender.send_command(cfg.MANIPULATOR_SET_DOWN_POSITION)
    sender.send_command(cfg.MANIPULATOR_OPEN_CLAW)
    stream = requests.get("http://192.168.2.156:8080/?action=stream", stream=True)
    if stream.status_code == 200:
        bytes = bytes()
        i = 0
        for chunk in stream.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8') # Начало jpeg
            b = bytes.find(b'\xff\xd9') # Конец jpeg
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2. IMREAD_COLOR)

                center = find_red_cube(img)
                if center is not None:
                    cv2.circle(img, center, 5, (0, 255, 0), -1)
                    cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 0, 255), 2)


                    message = cfg.MOTOR_STOP

                    x = center[0]
                    y = center[1]
                    if x <= 325:
                        message = cfg.MOTOR_LEFT_ON_PLACE
                    elif x > 360:
                        message = cfg.MOTOR_RIGHT_ON_PLACE
                    elif y > 350:
                        message = cfg.MOTOR_BACKWARD
                    elif y < 325:
                        message = cfg.MOTOR_FORWARD
                    else:
                        message = cfg.MANIPULATOR_GRAB
                        asyncio.run(send_move(sender, message))
                        break

                    if i == 0:
                        i = 0
                        print("1")
                        asyncio.run(send_move(sender, message))
                    i += 1
                    if i == 3:
                        i = 0

                cv2.imshow('img', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


if __name__ == '__main__':
    run()





# while (True):
#     ret, frame = cap.read()
#
#     center = find_red_cube(frame)
#
#     if center is not None:
#         cv2.circle(frame, center, 5, (0, 255, 0), -1)
#         cv2.putText(frame, "Center: ({}, {})".format(center[0], center[1]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                     (0, 0, 255), 2)
#
#     cv2.imshow('Video', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
