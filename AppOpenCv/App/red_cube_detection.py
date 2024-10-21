from time import sleep

from RobotCamera import RobotCamera

import cv2
import numpy as np

import config as cfg
from sender_without_logger import Sender

def find_blue_button(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([110, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

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
    sender = Sender("192.168.2.156", 4141)
    sender.send_command(cfg.MANIPULATOR_SET_DOWN_POSITION)
    sender.send_command(cfg.MANIPULATOR_OPEN_CLAW)

    # robot_camera = RobotCamera()
    # camera_thread = threading.Thread(target=robot_camera.start_read)
    # camera_thread.daemon = True
    # camera_thread.start()


    while True:
        test_cam_read = RobotCamera()
        img = test_cam_read.read()
        center = find_blue_button(img)
        if center is not None:
            cv2.circle(img, center, 5, (0, 255, 0), -1)
            cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)

        message = cfg.MOTOR_STOP
        if center is not None:
            x = center[0]
            y = center[1]
            if x <= 250:
                message = cfg.MOTOR_LEFT_ON_PLACE
            elif x > 275:
                message = cfg.MOTOR_RIGHT_ON_PLACE
            elif y > 280:
                message = cfg.MOTOR_BACKWARD
            elif y < 260:
                message = cfg.MOTOR_FORWARD
            else:
                message = cfg.MANIPULATOR_GRAB
                sender.send_command(message)
                break
            sender.send_command(message)
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def press_button():
    sender = Sender("192.168.2.156", 4141)
    sender.send_command(cfg.MANIPULATOR_DEFAULT_POSITION)
    sender.send_command(cfg.MANIPULATOR_CLOSE_CLAW)

    while True:
        test_cam_read = RobotCamera()
        img = test_cam_read.read()
        center = find_blue_button(img)
        if center is not None:
            cv2.circle(img, center, 5, (0, 255, 0), -1)
            cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)

        message = cfg.MOTOR_STOP
        if center is not None:
            x = center[0]
            y = center[1]
            if x <= 235:
                message = cfg.MOTOR_LEFT_ON_PLACE
            elif x > 245:
                message = cfg.MOTOR_RIGHT_ON_PLACE
            elif y > 260:
                message = cfg.MOTOR_BACKWARD
            elif y < 240:
                message = cfg.MOTOR_FORWARD
            else:
                message = cfg.MANIPULATOR_SET_THROW_POSITION
                sender.send_command(message)
                sleep(2)
                message = cfg.MANIPULATOR_DEFAULT_POSITION
                sender.send_command(message)
            sender.send_command(message)
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    press_button()





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
