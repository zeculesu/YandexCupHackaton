
import time
import cv2
import numpy as np
import requests


def read():
    start = time.time()
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
                print(time.time() - start)
                return img


# while True:
#     img = read()
#     # if center is not None:
#     #     cv2.circle(img, center, 5, (0, 255, 0), -1)
#     #     cv2.putText(img, "Center: ({}, {})".format(center[0], center[1]), (10, 30),
#     #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#     #                 (0, 0, 255), 2)
#
#     cv2.imshow('img', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break