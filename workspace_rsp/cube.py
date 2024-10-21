from time import sleep

import requests
import cv2
import numpy as np
# from manipulator import ManipulatorController
# from motor import MotorController

def read():
    global boobs
    stream = requests.get("http://0.0.0.0:8080/?action=stream", stream=True)
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

def find_red_cube(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 178, 130])
    upper_red = np.array([179, 255, 255])
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
    # motor = MotorController()
    # manipulator = ManipulatorController()
    # manipulator.set_down_position()
    # manipulator.open_claw()
    try:
        cv = cv2.VideoCapture(0)
        while True:
            ret, img = cv.read()
            # img = read()
            if not ret:
                break
            center = find_red_cube(img)
            if center is not None:
                cv2.circle(img, center, 5, (0, 255, 0), -1)
                cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)

            # motor.stop()
            if center is not None:
                x = center[0]
                y = center[1]
                if x <= 325:
                    print("left")
                    # motor.left_on_place()
                elif x > 360:
                    print("right")
                    # motor.right_on_place()
                elif y > 350:
                    print("backward")
                    # motor.backward()
                elif y < 325:
                    print("forward")
                    # motor.forward()
                else:
                    print("grab")
                    # motor.forward(4)
                    # manipulator.grab_cube()
                    # sleep(0.2)
                    # manipulator.set_default_position()
                    break
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        # motor.stop()
        quit()

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
