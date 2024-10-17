import cv2
import numpy as np
from client.sender import Sender


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


host, port = "192.168.2.156", 4242
sender = Sender(host, port)
while True:
    try:
        is_connect = sender.start_client()
        if is_connect:
            break
    except:
        continue

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Не удалось открыть видеопоток")

while (True):
    ret, frame = cap.read()

    center = find_red_cube(frame)

    if center is not None:
        cv2.circle(frame, center, 5, (0, 255, 0), -1)
        cv2.putText(frame, "Center: ({}, {})".format(center[0], center[1]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
